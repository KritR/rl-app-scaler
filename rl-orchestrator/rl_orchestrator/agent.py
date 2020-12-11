import orchestrator as o
from tensorforce import Agent, Environment
import pickle

env = o.Orchestrator()
env.seed(123)


model_dir = './data/m1/'

num_ep = 100
max_ep_ts = 200

# Pre-defined or custom environment
environment = Environment.create(
    environment='gym', level=env, max_episode_timesteps=max_ep_ts
)

# Instantiate a Tensorforce agent
agent = Agent.create(
    agent='ppo',
    environment=environment,  # alternatively: states, actions, (max_episode_timesteps)
    batch_size=4,
    saver=dict(
        directory=(model_dir + 'checkpoints'),
        frequency=2  # save checkpoint every 10 updates
    ),
)


output = []
# Train for 3 episodes with 100 timesteps each
for i in range(num_ep):

    # Initialize episode
    states = environment.reset()
    terminal = False

    rs = []
    costs = []
    ls = []
    survival = 0
    while not terminal:
        # Episode timestep
        actions = agent.act(states=states)
        states, terminal, reward = environment.execute(actions=actions)
        rs.append(reward)
        ls.append(states[5])
        costs.append(states[2])
        agent.observe(terminal=terminal, reward=reward)
        survival += 1

    print(f'Total Reward for episode {i} is {sum(rs)}')

    output.append((i,survival, rs, costs, ls))
    with open(model_dir + 'data.pickle', 'wb') as f:
        pickle.dump(output, f)

print(output)


"""
environment.train(agent=agent,
              num_episodes=num_ep, max_episode_timesteps=max_ep_ts,
              weights_dir=model_dir + 'weights', record_dir=model_dir + 'record')
"""

agent.save("./data/m1/final", "final-model")
agent.close()
environment.close()


