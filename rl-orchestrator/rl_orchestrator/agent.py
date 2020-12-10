import orchestrator as o
from tensorforce import Agent, Environment

env = o.Orchestrator()
env.seed(123)


# Pre-defined or custom environment
environment = Environment.create(
    environment='gym', level=env, max_episode_timesteps=100
)

# Instantiate a Tensorforce agent
agent = Agent.create(
    agent='tensorforce',
    environment=environment,  # alternatively: states, actions, (max_episode_timesteps)
    memory=1000,
    update=dict(unit='timesteps', batch_size=64),
    optimizer=dict(type='adam', learning_rate=3e-4),
    policy=dict(network='auto'),
    objective='policy_gradient',
    reward_estimation=dict(horizon=20),
    saver=dict(
        directory='data/checkpoints',
        frequency=100  # save checkpoint every 100 updates
    ),
)

# Train for 3 episodes with 100 timesteps each
for _ in range(3):

    # Initialize episode
    states = environment.reset()
    terminal = False

    while not terminal:
        # Episode timestep
        actions = agent.act(states=states)
        states, terminal, reward = environment.execute(actions=actions)
        agent.observe(terminal=terminal, reward=reward)

agent.close()
environment.close()


