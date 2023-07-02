import numpy as np
import os
import time

from colorama import Back
import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils.env_checker import check_env

from settings import *


class MapEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(self, change_perc, time_limit, render_mode="ansi"):
        super().__init__()
        total_tiles = len(level_map) * len(level_map[0])
        self.time_limit = time_limit # seconds
        self.observation_space = spaces.Dict(
            {
                "agent_location": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([len(level_map) - 1, len(level_map[0]) - 1]),
                    dtype=int,
                ),
                "current_tile": spaces.Discrete(n=4,start=0),
                "onehot_map": spaces.MultiBinary([total_tiles,4]),
                "remaining_time": spaces.MultiBinary([self.time_limit,])
            }
        )
        print(self.observation_space)
        self.action_space = spaces.Discrete(3)

        self.agent_actions = {
            0: 0,  # Empty Tile
            1: 1,  # Terrain Tile
            2: 2   # Coin Tile
        }

        # Change % limit
        self.change_perc = change_perc
        self.change_limit = int((self.change_perc/100) * total_tiles)

        # Target params
        self.target_jumps = 4
        self.target_coins = 6
        #self.target_isles = 2
        self.target_terrain = int(0.2 * total_tiles)

        self.rewards = {
            #"jumps": 20,
            "coins": 10,
            #"isles": 0,
            "terrain": 16,
            "bad_coin": -5,
            "bad_player": -6
        }

        # Some initializations
        self.current_time = int(time.time())
        self.time_vector = np.zeros(self.time_limit,dtype=int)
        self.reward = 0
        self.max_reward = self.rewards["coins"] + self.rewards["terrain"]

        # Jump Masks
        self.jump_masks = {
            0: np.array([[0,0,0],
                         [1,0,1],
                         [1,0,1]]),
            1: np.array([[0,0,0,0],
                         [1,0,0,1],
                         [1,0,0,1]]),
            2: np.array([[0,0,0,0,0],
                         [1,0,0,0,1],
                         [1,0,0,0,1]])
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def random_map(self, heigh, width, seed):
        generator = np.random.default_rng(seed)
        level = np.zeros(shape=(heigh,width),dtype=int)
        discount = 0
        density = np.random.randint(6,19) # higher is less terrain
        for i in range(heigh):
            for j in range(width):
                pick = generator.choice([0,1],p=[1-discount,discount])
                level[i][j] = pick
            discount += 1/(heigh+density)
        level[len(level)-3][0] = 3
        return level

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        print("Seed:",seed)
        self.map = self.random_map(11,28,seed)

        # Agent's random starting location
        self.agent_row = np.random.randint(0, len(self.map))
        self.agent_col = np.random.randint(0, len(self.map[0]))
        self.current_tile = self.map[self.agent_row][self.agent_col]

        # Reset counts
        self.terrain_count = 0
        self.coin_count = 0
        self.isle_count = 0
        self.jump_count = 0
        self.modified_tiles = 0
        self.bad_coins = 0
        for row in self.map:
            for col in row:
                if col == 1:
                    self.terrain_count += 1
                elif col == 2:
                    self.coin_count += 1

        # Adds time limit to timer
        self.finishing_time = int(self.current_time + self.time_limit)

        observation = {"agent_location": np.array([self.agent_row, self.agent_col]),
                       "current_tile": self.current_tile,
                       "onehot_map": self.encode_map(self.map),
                       "remaining_time": self.time_vector
                       }

        info = {}
        return observation, info

    def step(self, action):
        # Set angent's random location
        self.agent_row = np.random.randint(0, len(self.map))
        self.agent_col = np.random.randint(0, len(self.map[0]))

        os.system("cls")
        self.render()

        # Map the action (element of {0,1,2}) to the tile selected
        tile = self.agent_actions[action]
        
        aux = self.map[self.agent_row]
        self.current_tile = aux[self.agent_col]

        # Ignore player
        if self.current_tile != 3:
            aux[self.agent_col] = tile

            # Check if tile was modified and counts
            if tile != self.current_tile:
                self.modified_tiles += 1
                if tile == 1:
                    self.terrain_count += 1
                elif tile == 2:
                    self.coin_count += 1
                    if self.agent_row == 10:
                        self.bad_coins += 1
                        
                if self.current_tile == 1:
                    self.terrain_count -= 1
                elif self.current_tile == 2:
                    self.coin_count -= 1
                    if self.agent_row == 10:
                        self.bad_coins -= 1

        self.map[self.agent_row] = aux
        
        # Check if theres tiles under the player
        if (self.map[9][0] or self.map[10][0]) == 1:
            self.bad_player = 0
        else: 
            self.bad_player = 1

        #Calc reward
        self.reward = (
            1 - abs(self.target_terrain - self.terrain_count) / self.target_terrain) * self.rewards["terrain"] + (
            1 - abs(self.target_coins - self.coin_count) / self.target_coins) * self.rewards["coins"] + (
            self.bad_coins * self.rewards["bad_coin"]) + (
            self.bad_player * self.rewards["bad_player"])

        

        # An episode is done if the agent has reached the change %
        if (self.modified_tiles >= self.change_limit):
            """ for y in range(len(self.map)-2):
                for x in range(len(self.map[0])-2):
                    surround = self.map[np.ix_([y,y+1,y+2],[x,x+1,x+2])]
                    if np.array_equal(surround,self.jump_masks[0]):
                        self.jump_count += 1
                        x+=1

            self.reward += (
                1 - abs(self.target_jumps - self.jump_count) / self.target_jumps
            ) * self.rewards["jumps"] """
            terminated = True 
        else:
            terminated = False
        
        # Ending episode if time limit is reached
        self.current_time = int(time.time())
        rem = self.finishing_time - self.current_time
        if self.current_time > self.finishing_time:
            truncated = True
        else:
            truncated = False
            self.time_vector[rem-1] = 1

        observation = {"agent_location": np.array([self.agent_row, self.agent_col]),
                       "current_tile": int(self.current_tile),
                       "onehot_map": self.encode_map(self.map),
                       "remaining_time": self.time_vector
                       }

        os.system("cls")
        self.render()

        info = {
            "coins": self.coin_count,
            "bad coins": self.bad_coins,
            "terrain": self.terrain_count,
            "terrain target": self.target_terrain,
            "change limit": self.change_limit,
            "modified tiles": self.modified_tiles,
            "remaining time": rem
        }
        print(info)
        return observation, self.reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "ansi":
            for row,row_data in enumerate(self.map):
                print("| ",end="")
                for col,col_data in enumerate(row_data):
                    if (row == self.agent_row) and (col == self.agent_col):
                        print(Back.LIGHTRED_EX,end="")
                    if col_data == 0:
                        print(" ",end="")
                    elif col_data == 1:
                        print("X",end="")
                    elif col_data == 2:
                        print("C",end="")
                    else: print("P",end="")
                    print(Back.RESET,end="")
                print(" |")
            print("Reward: %7.4f" % (self.reward))
        
        print(end=Back.RESET)       
                
    def encode_map(self,map):
        aux = map.reshape(-1)
        oneHot = np.eye(4,dtype=int)[aux]
        return oneHot
        

if __name__ == "__main__":
    
    """ env = MapEnv(60,60)
    env.reset()
    done = False
    while done == False:
        observation, reward, terminated, truncated, info = env.step(np.random.randint(0,3))
        print(info)
        done = (terminated or truncated)

    check_env(env)  """
    
