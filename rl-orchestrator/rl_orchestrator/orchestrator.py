from enum import Enum
import logging
import random
import time
import node as n
import numpy as np
from gym import spaces, Env
from typing import Any, Dict, List, Tuple
import json
from subprocess import check_output

class Orchestrator(Env):
    """
    Define a simple orchestrator environment.
    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self) -> None:
        self.__version__ = "0.1.0"
        logging.info(f"Orchestrator - Version {self.__version__}")

        self.curr_step = -1

        self.IMAGE_NAME = "app-agent"
        self.MIN_NODES = 1
        self.MAX_NODES = 10
        self.ACTIONS = Enum('ACTIONS','UPGRADE_RAM UPGRADE_CPU DUPLICATE DOWNGRADE_RAM DOWNGRADE_CPU DESTROY REST')
        self.RAM_OPTS = [(0,64), (1,128), (2, 256)]
        self.CPU_OPTS = [(0,0.1), (1, 0.2), (2, 0.4)]

        self.action_space = spaces.Discrete(len(self.ACTIONS))

        # [node.cpu, node.ram, cost, cpu_load, mem_load, network_avg, network_worst]

        low = np.array([0, 0, 0, 0, 0, 0, 0])
        high = np.array([self.CPU_OPTS[-1][0], self.RAM_OPTS[-1][0], float('inf'), 2, 2, float('inf'), float('inf')])
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory: List[Any] = []

        self.nodes = set()
        for i in range(self.MIN_NODES):
            self._create_node(self.CPU_OPTS[0], self.RAM_OPTS[0])

        self.current_node = random.choice(tuple(self.nodes)) 


    def step(self, action: int) -> Tuple[List[int], float, bool, Dict[Any, Any]]:
        """
        The agent takes a step in the environment.
        Parameters
        ----------
        action : int
        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob : List[int]
                an environment-specific object representing your observation of
                the environment.
            reward : float
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over : bool
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info : Dict
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """

        self.curr_step += 1
        self._take_action(action)
        time.sleep(5)
        reward = self._get_reward()
        ob = self._get_state()

        return ob, reward, False, {}

    def _take_action(self, action: int) -> None:
        self.action_episode_memory[self.curr_episode].append(action)
        print("Taking action " + str(self.ACTIONS(action + 1).name))

        if action == self.ACTIONS['UPGRADE_RAM']:
            new_ram = self.current_node.ram[0] 
            if new_ram[0] + 1 < len(self.RAM_OPTS):
                new_ram = self.RAM_OPTS[new_ram[0] + 1]
            self._create_node(self.current_node.cpu, new_ram)
        elif action == self.ACTIONS['UPGRADE_CPU']:
            new_cpu = self.current_node.cpu[0] 
            if new_cpu[0] + 1 < len(self.CPU_OPTS):
                new_cpu = self.CPU_OPTS[new_cpu[0] + 1]
            self._create_node(new_cpu, self.current_node.ram)
        elif action == self.ACTIONS['DUPLICATE']:
            self._create_node(self.current_node.cpu, self.current_node.ram)
        elif action == self.ACTIONS['DOWNGRADE_RAM']:
            new_ram = self.current_node.ram[0] 
            if new_ram[0] > 0:
                new_ram = self.RAM_OPTS[new_ram[0] - 1]
            self._create_node(self.current_node.cpu, new_ram)
        elif action == self.ACTIONS['DOWNGRADE_CPU']:
            new_cpu = self.current_node.cpu[0] 
            if new_cpu[0] > 0:
                new_cpu = self.CPU_OPTS[new_cpu[0] - 1]
            self._create_node(new_cpu, self.current_node.ram)
        elif action == self.ACTIONS['DESTROY']:
            self._destroy_node(self.current_node)

        self.current_node = random.choice(tuple(self.nodes)) 

    def _get_reward(self) -> float:
        """Reward is given for a sold banana."""
        network_cost = - sum([n.cost for n in self.nodes]) # sum of node cost
        avg_lat, worst_lat = self._test_network()
        return ((1 * avg_lat) + (0.6 * worst_lat)) + (30*network_cost)

    def reset(self) -> List[int]:
        """
        Reset the state of the environment and returns an initial observation.
        Returns
        -------
        observation: List[int]
            The initial observation of the space.
        """
        self.curr_step = -1
        self.curr_episode += 1
        for n in self.nodes:
            n.destroy()
        self.nodes = set()
        for i in range(self.MIN_NODES):
            self._create_node(self.CPU_OPTS[0], self.RAM_OPTS[0])

        self.current_node = random.choice(tuple(self.nodes)) 
        self.action_episode_memory.append([])
        return self._get_state()

    def _render(self, mode: str = "human", close: bool = False) -> None:
        return None

    def _get_state(self) -> List[int]:
        """
        Cpu Level: n
        Ram Level: n
        Node cost: n
        Machine cpu load
        Machine ram load
        Network costs
        Network average Latency
        Network worst case latency
        """
        network_cost = sum([n.cost for n in self.nodes]) # sum of node cost
        network_avg, network_worst = self._test_network()
        cpu_load, mem_load, cost = self.current_node.query()

        return [self.current_node.cpu[0]/len(self.CPU_OPTS), self.current_node.ram[0]/len(self.RAM_OPTS), cost, cpu_load, mem_load, network_avg, network_worst]

    def _test_network(self):
        output = check_output("./test-nodes.sh").decode('utf-8')
        test_obj = json.loads(output)
        avg = int(test_obj['latencies']['mean']) / 10**6 # convert NS -> MS
        n_five = int(test_obj['latencies']['95th'])  / 10**6
        return avg, n_five

    def _create_node(self, cpu, ram):
        if len(self.nodes) >= self.MAX_NODES:
            return
        new_node = n.Node(self.IMAGE_NAME, cpu, ram)
        self.nodes.add(new_node)

    def _destroy_node(self, node):
        if len(self.nodes) <= self.MIN_NODES:
            return
        node.shutdown()
        self.nodes.remove(node)

    def seed(self, seed: int) -> None:
        random.seed(seed)
        np.random.seed(seed)


