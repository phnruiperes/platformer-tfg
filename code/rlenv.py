import numpy as np
import os

from colorama import Back
import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils.env_checker import check_env

from settings import *


class TestEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(self, render_mode="ansi"):
        super().__init__()
        total_tiles = len(level_map) * len(level_map[0])
        # Observations are dictionaries with the agent's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent_location": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([len(level_map) - 1, len(level_map[0]) - 1]),
                    dtype=int,
                ),
            }
        )
        print(self.observation_space)
        self.action_space = spaces.Discrete(3)

        self.agent_actions = {
            0: " ",  # Empty Tile
            1: "X",  # Terrain Tile
            2: "C",  # Coin Tile
        }

        #Change % limit
        self.change_limit = 0.4 * total_tiles

        # Target params
        self.target_jumps = 3
        self.target_coins = 6
        self.target_isles = 2
        self.target_terrain = 0.4 * total_tiles

        self.rewards = {
            "jumps": 8,
            "coins": 4,
            "isles": 6,
            "terrain": 10,
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.map = np.array(level_map, dtype=str)
        # Agent's starting location
        self.agent_row = np.random.randint(0,len(self.map))
        self.agent_col = np.random.randint(0,len(self.map[0]))

        # Reset counts
        self.terrain_count = 0
        self.coin_count = 0
        self.modified_tiles = 0

        # We will sample the target's location randomly until it does not coincide with the agent's location
        observation = {"agent_location": np.array([self.agent_row, self.agent_col])}

        info = {}
        return observation, info

    def step(self, action):
        # Set angent's random location
        self.agent_row = np.random.randint(0,len(self.map))
        self.agent_col = np.random.randint(0,len(self.map[0]))

        os.system("cls")
        self.render()

        # Map the action (element of {0,1,2}) to the tile selected
        tile = self.agent_actions[action]
        aux = list(self.map[self.agent_row])

        # Check if tile was modified
        if tile != aux[self.agent_col]:
            self.modified_tiles +=1
        
        if aux[self.agent_col] != "P":
            aux[self.agent_col] = tile
        self.map[self.agent_row] = "".join(aux)

        if action == 1:
            self.terrain_count += 1
        elif action == 2:
            self.coin_count += 1

        reward = (
            1 - abs(self.target_terrain - self.terrain_count) / self.target_terrain) * self.rewards["terrain"] + (
            1 - abs(self.target_coins - self.coin_count) / self.target_coins) * self.rewards["coins"]

        # An episode is done if the agent has reached the change %
        terminated = True if self.modified_tiles >= self.change_limit else False

        observation = {"agent_location": np.array([self.agent_row, self.agent_col])}

        os.system("cls")
        self.render()
        info = {}
        return observation, reward, terminated, info

    def render(self):
        if self.render_mode == "ansi":
            for row_index, row_data in enumerate(self.map):
                if row_index == self.agent_row:
                    print(end="| ")
                    for col_index, col_data in enumerate(row_data):
                        if col_index == self.agent_col:
                            print(end=Back.LIGHTRED_EX + col_data)
                        else:
                            print(end=Back.RESET + col_data)
                    print(" |")
                else:
                    print("|", row_data, "|")
        print(end=Back.RESET)


if __name__ == "__main__":
    testEnv = TestEnv()
    testEnv.reset()
    done = False
    while not done:
        training = testEnv.step(action=np.random.randint(0,3))
        print(training[1])
        done = training[2]

    #check_env(testEnv)
