from stable_baselines3 import PPO
import os
from rlenv import MapEnv

for change_perc in [20, 40, 60]:
    for time_limit in [15, 30, 60]:
        env = MapEnv(change_perc, time_limit)
        env.reset()

        models_dir = f"models/{env.change_perc}p{env.time_limit}s/"
        logdir = f"logs/{env.change_perc}p{env.time_limit}s/"

        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        if not os.path.exists(logdir):
            os.makedirs(logdir)

        TIMESTEPS = 1000

        model = PPO(
            "MultiInputPolicy",
            env,
            verbose=1,
            tensorboard_log=logdir,
            device="cuda",
            n_steps=100,
        )  # n_steps better if lower than episode length

        # total =  i * TIMESTEPS
        for i in range(1, 101):
            model.learn(
                total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO"
            )
            model.save(f"{models_dir}/{TIMESTEPS*i}")
