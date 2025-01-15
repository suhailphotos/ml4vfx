import gym
import os
import wandb
from gym.wrappers import GrayScaleObservation
from wandb.integration.sb3 import WandbCallback
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder, VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

env_name = "BipedalWalker-v3"
config = {
    "policy_type": "MlpPolicy",
    "total_timesteps": 350000,
    "env_name": env_name
        }

def make_env():
    env = gym.make(config["env_name"], render_mode="rgb_array")
    #env = Monitor(env)
    return env


run = wandb.init(
    project="bipedal_gym",
    config=config,
    sync_tensorboard=True,
    monitor_gym=True,
    save_code=True
        )

env = DummyVecEnv([make_env])
env = VecVideoRecorder(env, f"videos/{run.id}", record_video_trigger=lambda x:x %200==0, video_length=200)

model = PPO(config['policy_type'], env, verbose=1, tensorboard_log=f"runs/{run.id}")
model.learn(
    total_timesteps=config["total_timesteps"],
    callback=WandbCallback(gradient_save_freq=100, model_save_path=f"models/{run.id}", verbose=2
    ),)

PPO_path = os.path.join('Training', 'Saved Models', 'PPO_BipedalWalker_350k')
model.save(PPO_path)

evaluate_policy(model, env, n_eval_episodes=20, render=True)
run.finish()
