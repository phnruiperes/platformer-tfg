import numpy as np

from stable_baselines3 import PPO
from rlenv import MapEnv

models_dir = "models"

for change_perc in [60]:
    for time_limit in [60]:
        env = MapEnv(change_perc, time_limit)
        env.reset()

        model_path = f"{models_dir}/{env.change_perc}p{env.time_limit}s/80000"
        model = PPO.load(model_path, env=env)

        maps = 20

        f = open(f"maps/maps_file_{env.change_perc}p{env.time_limit}s.py", "w")
        f.write('maps = {\n')
        f.close()
        
        for map in range(maps):
            obs, info = env.reset()
            done = False
            while not done:
                action = model.predict(obs)
                obs, reward, term, trunc, info = env.step(int(action[0]))
                done = term or trunc

            f = open(f"maps/maps_file_{env.change_perc}p{env.time_limit}s.py", "a")
            f.write(f'    "map_{map}" : {np.ndarray.tolist(env.map)},\n')
            f.close()
        
        f = open(f"maps/maps_file_{env.change_perc}p{env.time_limit}s.py", "a")
        f.write('}')
        f.close()

