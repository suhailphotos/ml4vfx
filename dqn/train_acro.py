import gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

env = gym.make('Acrobot-v1')
env = DummyVecEnv([lambda: env])

#train
model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

#save model
model.save('dqn_acrobot')

