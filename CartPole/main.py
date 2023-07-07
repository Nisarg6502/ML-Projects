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
angles = []

for episodeIndex in range(episodeNumber):
    # reset the environment for each episode
    state = env.reset()
    print(f"Episode {episodeIndex}")
    env.render()  # render the environment
    for timeIndex in range(timeSteps):
        random_action = env.action_space.sample()  # we perform a random action
        observation, reward, terminated, truncated, info = env.step(
            random_action)  # we collect the info of each step
        positions.append(observation[0])
        angles.append(np.degrees(observation[2]))  # Convert angle to degrees
        time.sleep(0.1)
        if terminated:
            time.sleep(1)
            break

# Plot the cart positions
plt.subplot(2, 1, 1)
plt.plot(positions)
plt.xlabel('Time Step')
plt.ylabel('Cart Position')
plt.title('Cart Position over Time')

# Plot the pole angles
plt.subplot(2, 1, 2)
plt.plot(angles)
plt.xlabel('Time Step')
plt.ylabel('Pole Angle (Degrees)')
plt.title('Pole Angle over Time')

plt.tight_layout()
plt.show()
