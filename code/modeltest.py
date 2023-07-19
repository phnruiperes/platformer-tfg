import numpy as np

from stable_baselines3 import PPO
from rlenv import MapEnv
from check_maps import check_maps

def generate_maps(change_perc,time_limit,qnt):
    env = MapEnv(change_perc, time_limit)
    env.reset()

    model_path = f"models/{env.change_perc}p{env.time_limit}s/90000"
    model = PPO.load(model_path, env=env)

    maps = qnt

    f = open(f"maps_file_{env.change_perc}p{env.time_limit}s.py", "w")
    f.write('maps = {\n')
    f.close()

    for map in range(maps):
        obs, info = env.reset()
        done = False
        while not done:
            action = model.predict(obs)
            obs, reward, term, trunc, info = env.step(int(action[0]))
            done = term or trunc

        f = open(f"maps_file_{env.change_perc}p{env.time_limit}s.py", "a")
        f.write(f'    "map_{map}" : {np.ndarray.tolist(env.map)},\n')
        f.close()

    f = open(f"maps_file_{env.change_perc}p{env.time_limit}s.py", "a")
    f.write('}')
    f.close()

if __name__ == "__main__":
    QNT=10
    generate_maps(60,15,QNT)

    from maps_file_60p15s import *

    check_maps(maps,QNT)

