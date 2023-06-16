
from stable_baselines3 import PPO
import os
from rlenv import MapEnv
import time

models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logdir):
	os.makedirs(logdir)
	
env = MapEnv()
env.reset()

model = PPO('MultiInputPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS=1000

for i in range(50):
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save(f"{models_dir}/{TIMESTEPS*i}")
