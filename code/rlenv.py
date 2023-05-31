import numpy as np
import os

from colorama import Back
import gymnasium as gym
from gymnasium import spaces

from settings import *

class TestEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(self,render_mode="ansi"):
        super().__init__()
        total_tiles = len(level_map) * len(level_map[0])
        # Observations are dictionaries with the agent's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent_location": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([len(level_map), len(level_map[0])]),
                    dtype=int,
                ),
            }
        )

        self.action_space = spaces.Discrete(3)

        self.agent_actions = {
            0: " ",  # Empty Tile
            1: "X",  # Terrain Tile
            2: "C",  # Coin Tile
        }

        # Target params
        self.target_jumps = 3
        self.target_coins = 6
        self.target_terrains = 0.4 * total_tiles

        self.rewards = {}

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.map = np.array(level_map, dtype=str)
        # Choose the agent's location
        self.agent_row = 0
        self.agent_col = 0

        # We will sample the target's location randomly until it does not coincide with the agent's location
        observation = {
            "agent (row,col)": (self.agent_row, self.agent_col),
            "map": self.map,
        }

        return observation

    def step(self, action):
        # Map the action (element of {0,1,2}) to the tyle selected
        tile = self.agent_actions[action]
        aux = list(self.map[self.agent_row])           
        aux[self.agent_col] = tile
        self.map[self.agent_row] = ''.join(aux)

        if self.agent_col >= len(self.map[0])-1:
            self.agent_row += 1
            self.agent_col = 0
        else:
            self.agent_col += 1

        # An episode is done iff the agent has reached the target
        terminated = True if self.agent_row >= len(self.map) else False

        observation = {
            "agent (row,col)": (self.agent_row, self.agent_col),
            "map": self.map,
        }
        
        os.system('cls')
        self.render()
        reward = None
        return observation, reward, terminated
    
    def render(self):
        if self.render_mode == "ansi":
            for row_index,row_data in enumerate(self.map):
                if row_index == self.agent_row:
                    print(end='| ')
                    for col_index,col_data in enumerate(row_data):
                        if col_index == self.agent_col:
                            print(end=Back.LIGHTRED_EX+col_data)
                        else:
                            print(end=Back.RESET+col_data)
                    print(' |')
                else:
                    print('|',row_data,'|')
        print(end=Back.RESET)


""" if __name__ == "__main__":
    testEnv = TestEnv()
    testEnv.reset()
    done = False
    while not done:
        done = testEnv.step(action=np.random.randint(0,3))[2] """
    
    
    
