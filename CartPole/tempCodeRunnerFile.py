import gym
import numpy as np
import time
import matplotlib.pyplot as plt

# create environment
env = gym.make('CartPole-v1', render_mode='rgb_array')

# reset the environment, returns an initial state
(state, _) = env.reset()

# render the environment
env.render()

# push cart in one direction
env.step(0)

# simulate the environment
episodeNumber = 5
timeSteps = 100
positions = []

for episodeIndex in range(episodeNumber):
    # reset the environment for each episode
    state = env.reset()
    print(f"Episode {episodeIndex}")
    env.render()
    for timeIndex in range(timeSteps):
        random_action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(
            random_action)
        positions.append(observation[0])
        time.sleep(0.1)
        if terminated:
            time.sleep(1)
            break

# Plot the cart positions
plt.plot(positions)
plt.xlabel('Time Step')
plt.ylabel('Cart Position')
plt.title('Cart Position over Time')
plt.show()
