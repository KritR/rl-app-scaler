# RL Based Docker App Scaler

This project uses reinforcement learning to automatically scale an application up or down.
This is currently a centralized system for testing.
However the goal is to connect the environment provider to cloud providers,
so applications can essentially run themselves.

# Dependencies

The projects main dependencies are poetry, docker, k6, and vegeta.

Poetry is used for installing the python packages.
Docker is used to run the contain instances.
K6 and Vegeta are both used for load testing and environment simulation.

# Setup

In order to run the project, we must first build the containers, instantiate the environment, and then run thy python.

```
docker build -t app-agent ./app-agent/
docker build -t lb ./app-agent/load_balancer/
docker network create rl-test
docker run -p 5000:80 --network=rl-test --name load_bal lb
```

Then we can actually run the agent to initialize the training.

```
python ./rl-orchestrator/rl_orchestrator/agent.py
```

finally the following command to apply a network load on the environment.

```
k6 ./rl-orchestrator/http-test.js
```
