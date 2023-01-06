def parse_input(filename):
    with open(filename, "r") as f:
        parsed_input = f.read()
    return parsed_input

import numpy as np
DEBUG = True

'''
Get stone pattern based on the sequence
'''
NUM_STONE_PATTERNS = 5
def get_stone_pattern(seq_id):
    seq_id = seq_id % NUM_STONE_PATTERNS
    # assuming that stone always starts 2 steps away from left, in a cave of length 7
    stone_pattern={}
    if seq_id==0:
        # pattern of -, 0b0011110
        stone_pattern ={
            "start": 2,
            "end": 5,
            "pattern": np.array([30], dtype="uint16")
        }
    elif seq_id == 1:
        # pattern of +, 
        # [0b0001000, 
        #  0b0011100, 
        #  0b0001000]
        stone_pattern ={
            "start": 2,
            "end": 4,
            "pattern": np.array([8, 28, 8], dtype="uint16")
        }
    elif seq_id == 2:
        # pattern of mirror L, 
        # [0b0000100, 
        #  0b0000100, 
        #  0b0011100]
        stone_pattern ={
            "start": 2,
            "end": 4,
            "pattern": np.array([28, 4, 4], dtype="uint16")
        }
    elif seq_id == 3:
        # pattern of |, 
        # [0b0010000,
        #  0b0010000,
        #  0b0010000,
        #  0b0010000]
        stone_pattern ={
            "start": 2,
            "end": 2,
            "pattern": np.array([16, 16, 16, 16], dtype="uint16")
        }
    elif seq_id == 4:
        # pattern of #, 
        # [0b0011000,
        #  0b0011000]
        stone_pattern ={
            "start": 2,
            "end": 3,
            "pattern": np.array([24, 24], dtype="uint16")
        }
    else:
        raise ValueError("Incorrect stone pattern")
    return stone_pattern

def visualize_pattern(pattern):
    # cave_state is a numpy array
    print("$"*10)
    for i in range(pattern.size):
        print(bin(pattern[i]))
    print("$"*10)

'''
Function to simulate 1 step of the rock falling
curr_cave_state: current state of the cave
curr_rock_type: shape and position of the falling rock
returns:
next_cave_state: updated state of the cave,
next_rock_state:
status: if the current rock settled in the cave or not, True if settled, False if not
'''
def detect_collision(cave, stone_pattern, height_from_ceiling):
    start_idx = -(height_from_ceiling+stone_pattern.size)
    if np.abs(start_idx) == cave.size + 1:
        #reached the end of the cave
        return False
    end_idx = None if height_from_ceiling==0 else -height_from_ceiling
    no_collission = np.sum((cave[start_idx:end_idx] & stone_pattern)!=0)==0
    return no_collission

def update_cave(cave, stone_pattern, height_from_ceiling):
    start_idx = -(height_from_ceiling+stone_pattern.size)
    end_idx = None if height_from_ceiling==0 else -height_from_ceiling
    cave[start_idx:end_idx] = cave[start_idx:end_idx]|stone_pattern
    return cave

CAVE_LENGTH = 7
def simulate_stone_fall(cave, stone_pattern, current_jet_stream, height_from_ceiling):
    shift = 0
    if current_jet_stream == "<":
        shift = -1
    if current_jet_stream == ">":
        shift = +1
    start = stone_pattern["start"]
    end = stone_pattern["end"]
    if start+shift <0 or end+shift>CAVE_LENGTH-1:
        #stone hit the border, dont apply jet stream effect
        ...
    else:
        new_pattern = stone_pattern["pattern"] >> 1 if shift == 1 else stone_pattern["pattern"] << 1 
        no_collission = detect_collision(cave, new_pattern, height_from_ceiling)
        if no_collission:
            #jet effect applicable to stone pattern
            stone_pattern["start"] += shift
            stone_pattern["end"] += shift
            stone_pattern["pattern"] = new_pattern
        else:
            #the jet didnt affect the stone. Check for vertical fall next
            ...
    if (detect_collision(cave, stone_pattern["pattern"], height_from_ceiling+1)):
        #stone continues to fall
        return cave, stone_pattern, False
    else:
        #stone hit the boundary
        cave = update_cave(cave, stone_pattern["pattern"], height_from_ceiling)
        return cave, stone_pattern, True

def simulate_cave(input_jet_stream, num_stones):
    ## Start with an empty cave. Append the rows per the stone size
    max_jet_stream_len = len(input_jet_stream)
    cave = np.zeros(0, dtype="uint16")
    visualize_pattern(cave)
    time_step = 0
    stack_height = 0
    for i in range(num_stones):
        height_from_ceiling = 0
        stone_pattern = get_stone_pattern(i)
        if DEBUG:
            print("shape of the falling stone")
            visualize_pattern(stone_pattern["pattern"])
        required_cave_height = stack_height + 3 + stone_pattern["pattern"].size
        offset = cave.size - required_cave_height
        if offset > 0:
            height_from_ceiling = offset
        elif offset < 0:
            cave = np.concatenate((cave, np.zeros(-offset, dtype="uint16")))
        fall_complete = False
        #TODO: First 3 fall iterations can be optimized as it guarantees no interaction with other cave stones
        while (not fall_complete):
            cave, stone_pattern, fall_complete = simulate_stone_fall(cave, stone_pattern, input_jet_stream[time_step], height_from_ceiling)
            height_from_ceiling+=1
            time_step+=1
            if time_step == max_jet_stream_len:
                time_step = 0
        stack_height = max(stack_height, cave.size - height_from_ceiling + 1)
        if DEBUG:
            print("State of the cave:")
            visualize_pattern(cave)
            print("Height of the cave after {} stones is {}".format(i+1, stack_height))

    return stack_height

if __name__=="__main__":
    input_file = "17_1_input.txt"
    input_file = "17_1_example_input.txt"
    input_jet_stream = parse_input(input_file)
    num_stones = 1000000000000
    DEBUG = False
    stack_height = simulate_cave(input_jet_stream, num_stones=num_stones)
    print("Height of the cave after {} stones is {}".format(num_stones, stack_height))
