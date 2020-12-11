from enum import Enum
import logging
import random
import time
import math
import node as n
import numpy as np
from gym import spaces, Env
from typing import Any, Dict, List, Tuple
import json
from subprocess import check_output

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

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
        self.INTOLERABLE_LATENCY = 5 * 1000 # 5 seconds 
        self.ACTIONS = Enum('ACTIONS','UPGRADE_RAM UPGRADE_CPU DUPLICATE DOWNGRADE_RAM DOWNGRADE_CPU DESTROY REST')
        self.RAM_OPTS = [(i, (i+1) * 32) for i in range(10)]
        self.CPU_OPTS = [(i, round((i+1) * 0.05,2)) for i in range(10)]
        self.MAX_COST = 2 * self.MAX_NODES * (len(self.RAM_OPTS) * 2  + len(self.CPU_OPTS))

        self.action_space = spaces.Discrete(len(self.ACTIONS))

        # [node.cpu, node.ram, cost, cpu_load, mem_load, network_avg, network_worst, node_capacity]

        low = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([1, 1, 1, 2, 2, 1, 1, 1])
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory: List[Any] = []

        self.prev_cost = 0

        self.nodes = set()
        for i in range(self.MIN_NODES):
            self._create_node(self.CPU_OPTS[len(self.CPU_OPTS)//2], self.RAM_OPTS[len(self.RAM_OPTS)//2])

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
        action_applied = self._take_action(action)
        time.sleep(8)
        reward = self._get_reward(action)
        ob = self._get_state()

        return ob, reward, not action_applied, {}

    def _take_action(self, action: int) -> bool:
        self.action_episode_memory[self.curr_episode].append(action)

        action_enum_val = action + 1
        print("Taking action " + str(self.ACTIONS(action_enum_val).name))

        action_applied = False
        if action_enum_val == self.ACTIONS.UPGRADE_RAM.value:
            print("upgrading ram")
            new_ram = self.current_node.ram
            if new_ram[0] + 1 < len(self.RAM_OPTS):
                new_ram = self.RAM_OPTS[new_ram[0] + 1]
                action_applied = True
            action_applied = action_applied and self._create_node(self.current_node.cpu, new_ram)
        elif action_enum_val == self.ACTIONS.UPGRADE_CPU.value:
            print("upgrading cpu")
            new_cpu = self.current_node.cpu
            if new_cpu[0] + 1 < len(self.CPU_OPTS):
                new_cpu = self.CPU_OPTS[new_cpu[0] + 1]
                action_applied = True
            action_applied = action_applied and self._create_node(new_cpu, self.current_node.ram)
        elif action_enum_val == self.ACTIONS.DUPLICATE.value:
            print("duplicating")
            action_applied = self._create_node(self.current_node.cpu, self.current_node.ram)
        elif action_enum_val == self.ACTIONS.DOWNGRADE_RAM.value:
            print("downgrading ram")
            new_ram = self.current_node.ram
            if new_ram[0] > 0:
                action_applied = True
                new_ram = self.RAM_OPTS[new_ram[0] - 1]
            action_applied = action_applied and self._create_node(self.current_node.cpu, new_ram)
        elif action_enum_val == self.ACTIONS.DOWNGRADE_CPU.value:
            print('downgrading cpu')
            new_cpu = self.current_node.cpu
            if new_cpu[0] > 0:
                new_cpu = self.CPU_OPTS[new_cpu[0] - 1]
                action_applied = True
            action_applied = action_applied and self._create_node(new_cpu, self.current_node.ram)
        elif action_enum_val == self.ACTIONS.DESTROY.value:
            print('destroying node')
            action_applied = self._destroy_node(self.current_node)
        else:
            action_applied = True
            print("No action chosen")

        self.current_node = random.choice(tuple(self.nodes)) 
        return action_applied

    def _get_reward(self, action) -> float:
        """Reward is given for a sold banana."""
        network_cost = sum([n.cost for n in self.nodes]) # sum of node cost
        avg_lat, worst_lat = self._test_network()
        total_cost = ((1 * avg_lat) + (0.6 * worst_lat)) + (network_cost)
        delta_cost = total_cost - self.prev_cost
        if self.prev_cost == 0:
            delta_cost = 0
        self.prev_cost = total_cost
        if (action+1) == self.ACTIONS.REST.value:
          delta_cost -= 30
        print(f"Network Cost : {network_cost} | Avg Lat : {avg_lat} | 95th Lat : {worst_lat}")
        print(f"Reward is {-delta_cost}")
        return -delta_cost

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
        self.prev_cost = 0
        for n in self.nodes:
            n.destroy()
        self.nodes = set()
        for i in range(self.MIN_NODES):
            self._create_node(self.CPU_OPTS[len(self.CPU_OPTS)//2], self.RAM_OPTS[len(self.RAM_OPTS)//2])

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
        normalized_cpu_lvl = self.current_node.cpu[0]/len(self.CPU_OPTS)
        normalized_mem_lvl = self.current_node.ram[0]/len(self.RAM_OPTS)
        normalized_cost = min(cost, self.MAX_COST) / self.MAX_COST
        normalized_net_avg = min(network_avg, self.INTOLERABLE_LATENCY) / self.INTOLERABLE_LATENCY
        normalized_net_worst = min(network_worst, self.INTOLERABLE_LATENCY) / self.INTOLERABLE_LATENCY
        normalized_node_cap = len(self.nodes) / (self.MAX_NODES + 1)

        return [normalized_cpu_lvl, normalized_mem_lvl, normalized_cost, cpu_load, mem_load, normalized_net_avg, normalized_net_worst, normalized_node_cap]

    def _test_network(self):
        output = check_output("./test-nodes.sh").decode('utf-8')
        test_obj = json.loads(output)
        avg = int(test_obj['latencies']['mean']) / 10**6 # convert NS -> MS
        n_five = int(test_obj['latencies']['95th'])  / 10**6
        return avg, n_five

    def _create_node(self, cpu, ram) -> bool:
        if len(self.nodes) >= self.MAX_NODES:
            return False
        new_node = n.Node(self.IMAGE_NAME, cpu, ram)
        self.nodes.add(new_node)
        return True

    def _destroy_node(self, node) -> bool:
        if len(self.nodes) <= self.MIN_NODES:
            return False
        node.destroy()
        self.nodes.remove(node)
        return True

    def seed(self, seed: int) -> None:
        random.seed(seed)
        np.random.seed(seed)


