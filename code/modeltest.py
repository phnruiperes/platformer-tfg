import gymnasium as gym
from stable_baselines3 import PPO
from rlenv import MapEnv

models_dir = "models"

env = MapEnv()
env.reset()

model_path = f"{models_dir}/1686865090/70000"
model = PPO.load(model_path, env=env)

episodes = 1

for ep in range(episodes):
    obs, info = env.reset()
    done = False
    while not done:
        action = model.predict(obs)
        obs, reward, done, trunc, info = env.step(int(action[0]))
        print("Reward: %7.4f" % (reward))

    print(info)
    #Converter env.map em vetor de strings e dar append num arquivo com os mapas numerados
