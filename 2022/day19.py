GLOBAL_INDEX_ORDER = ["ore", "clay", "obsidian", "geode"]
import numpy as np
'''
Function to calculate score of the given blueprint.
Input:
a cross table with rows denoting cost for each type of robot.
Types of robot (in order) are: "ore", "clay", "obsidian", "geode"
'''
def find_possible_new_robots(blueprint, time, robots, resources):
    possible_combinations=[]
    end_idx = -1
    if time <=3:
        end_idx = 2
    is_valid_combination = np.sum(blueprint - resources > 0, axis=-1)==0
    # heurisitic to check if we have enough resources of a particular kind 
    # to manufacture geode robot every minute  from the current state
    if time == 4:
        is_useless = (resources >= (time - 2)*blueprint[-1])
        is_useless[-1] = 0
        is_valid_combination = is_valid_combination & (1 - is_useless)
    t_remaining = (time - 2)
    max_possible_resources = t_remaining * robots + t_remaining * (t_remaining-1)/2
    # is_zero_geode_path = np.sum((blueprint[-1] > (max_possible_resources + resources))[:-1])>0 and resources[-1]==0 and robots[-1]==0
    # if is_zero_geode_path and time >2:
    #     return possible_combinations
    for i in range(blueprint.shape[0] - 1, end_idx, -1):
        if is_valid_combination[i]:
            new_robot = np.zeros(len(GLOBAL_INDEX_ORDER))
            new_robot[i] = 1
            #if we can manufacture geode collecting robot, stop looking for other possibilities
            if i == blueprint.shape[0] - 1:
                possible_combinations.append([new_robot, resources-blueprint[i]])
                break
            if max_possible_resources[i] >= (blueprint[-1]- resources)[i]:
                possible_combinations.append([new_robot, resources-blueprint[i]])
        if i == blueprint.shape[0] - 1:
            # no need to explore a possibility of no new robots with 0 geodes at time ==2, and (not (time ==2 and resources[-1]==0))
            possible_combinations.append([np.zeros(len(GLOBAL_INDEX_ORDER)), resources])

    # if possible_combinations ==[]:
    #     possible_combinations.append([np.zeros(len(GLOBAL_INDEX_ORDER)), resources])
    # if time <=4:
    #     print("At time {}, {}, {}, {}, {}".format(time, robots, resources, max_possible_resources, possible_combinations))
        # print("possible combos at time ", time, robots, (possible_combinations))
    return possible_combinations


def get_score_recursive(blueprint, time, robots, resources):
    if time == 1:
        final_resource = resources+robots
        # print("terminal loop", resources, robots)
        return final_resource[-1], [[time-1, robots, resources + robots]]
    if time <= 3:
        if robots[-2] == 0: # if you dont have obsidian robots by this time, there is no chance to have a geode robot
            return 0, []

    possible_next_combinations = find_possible_new_robots(blueprint, time, robots, resources)
    max_future_cost = 0
    max_strategy = []
    if possible_next_combinations == []:
        # the current combination doesnt yield non-zero outcome
        return 0, []
    for next_combination in possible_next_combinations:
        # if is_useful(next_combination):
        next_cost, info_list = get_score_recursive(blueprint, time - 1, robots+next_combination[0], next_combination[1] + robots)
        if max_future_cost <= next_cost:
            max_future_cost = next_cost
            max_strategy = info_list +[[time-1, robots+next_combination[0], next_combination[1] + robots]]
    # print(time, max_future_cost, final_resources, final_robots)
    return max_future_cost, max_strategy


def get_score(blueprint, time):
    # starting state is always ore = 1, resources = 0
    # robot count = [1, 0, 0, 0]
    # resources = [0, 0, 0, 0]
    # global_index_order = ["ore", "clay", "obsidian", "geode"]
    # Check if any new robots can be manufactured with current resources
    starting_resources = np.zeros(4)
    starting_robots = np.array([1, 0, 0, 0])
    return get_score_recursive(blueprint, time, starting_robots, starting_resources)


# Parse the input blueprints and arrange them by the resources required in every column for a given row
# follows GLOBAL_INDEX_ORDER
def parse_input(filename):
    with open(filename, "r") as f:
        parsed_input = f.readline()
    return parsed_input

if __name__=="__main__":
    input_file = "19_1_input.txt"
    input_blueprint_list = parse_input(input_file)
    blueprint_0 = np.array([
        [4, 0, 0, 0],
        [2, 0, 0 ,0],
        [3,14, 0, 0],
        [2, 0, 7, 0]])
    blueprint_1 = np.array([
        [2, 0, 0, 0],
        [3, 0, 0 ,0],
        [3, 8, 0, 0],
        [3, 0,12, 0]])
    print(get_score(blueprint_0, 20))
