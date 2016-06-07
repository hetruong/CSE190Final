# mdp implementation needs to go here
import copy

def intializePolicy(config_file):
    map_size = config_file["map_size"]
    board =  [["" for i in range(map_size[1])] for j in range(map_size[0])]
    for pit in config_file["pits"]:
        board[pit[0]][pit[1]] = "PIT"
    for wall in config_file["walls"]:
        board[wall[0]][wall[1]] = "WALL"
    goals = config_file["goals"]
    for goal in goals:
        board[goal[0]][goal[1]] =  "GOAL"
    return board
    
def initializeValue(config_file):
    map_size = config_file["map_size"]
    board =  [[0 for i in range(map_size[1])] for j in range(map_size[0])]
    
#     board.append([0 for i in range(map_size[1])])
#     board = [[0 for i in range(map_size[1])]] + board
#     for i in range(len(board)):
#         row = board[i]
#         row.append(0)
#         board[i] = [0] + row
    return board
    
def initializeReward(config_file):
    map_size = config_file["map_size"]
    path_cost = config_file["reward_for_each_step"]
    wall_hit = config_file["reward_for_hitting_wall"]
    goals = config_file["goals"]
    board =  [[path_cost for i in range(map_size[1])] for j in range(map_size[0])]
    for pit in config_file["pits"]:
        board[pit[0]][pit[1]] += config_file["reward_for_falling_in_pit"]
    for wall in config_file["walls"]:
        board[wall[0]][wall[1]] += wall_hit
    for i in range(len(goals)):
        goal = goals[i]
        board[goal[0]][goal[1]] = config_file["goal_rewards"][i]
    
#     board.append([wall_hit for i in range(map_size[1])])
#     board = [[wall_hit for i in range(map_size[1])]] + board
#     for i in range(len(board)):
#         row = board[i]
#         row.append(wall_hit)
#         board[i] = [wall_hit] + row
    return board

def calcMaxValue(config_file,currLoc,valueGrid,rewardGrid):
#     discount = config_file["discount_factor"]
    discount = 1
    walls = config_file["walls"]
    p_forward = config_file["prob_move_forward"]
    p_backward = config_file["prob_move_backward"]
    p_left = config_file["prob_move_left"]
    p_right = config_file["prob_move_right"]
    wall_hit = config_file["reward_for_hitting_wall"] + config_file["reward_for_each_step"]
    move_list = config_file["move_list"]
    currMax = -10000000000000;
    bestMove = []
    for move in move_list:
        #right
        currMove = ""
        if move == [0,1]:
            left = [currLoc[0]-1,currLoc[1]]
            right = [currLoc[0]+1,currLoc[1]]
            backward = [currLoc[0],currLoc[1]-1]
            forward = [currLoc[0],currLoc[1]+1]            
            currMove = "E"
        #left
        elif move == [0,-1]:
            left = [currLoc[0]+1,currLoc[1]]
            right = [currLoc[0]-1,currLoc[1]]
            backward = [currLoc[0],currLoc[1]+1]
            forward = [currLoc[0],currLoc[1]-1]
            currMove = "W"
            
        #down
        elif move == [1,0]:
            left = [currLoc[0],currLoc[1]+1]
            right = [currLoc[0],currLoc[1]-1]
            backward = [currLoc[0]-1,currLoc[1]]
            forward = [currLoc[0]+1,currLoc[1]]
            currMove = "S"
            
        #up
        elif move == [-1,0]:
            left = [currLoc[0],currLoc[1]-1]
            right = [currLoc[0],currLoc[1]+1]
            backward = [currLoc[0]+1,currLoc[1]]
            forward = [currLoc[0]-1,currLoc[1]]
            currMove = "N"
            
        

        if left[0] < 0 or left[0] >= len(valueGrid) or left[1] < 0 or left[1] >= len(valueGrid[0]) or left in walls:
            left_value = discount*valueGrid[currLoc[0]][currLoc[1]]
            left_reward = p_left*(wall_hit + left_value)
        else:
            left_value = discount*valueGrid[left[0]][left[1]]
            left_reward = p_left*(rewardGrid[left[0]][left[1]] + left_value)
           
        if right[0] < 0 or right[0] >= len(valueGrid) or right[1] < 0 or right[1] >= len(valueGrid[0]) or right in walls:
            right_value = discount*valueGrid[currLoc[0]][currLoc[1]]
            right_reward = p_right*(wall_hit + right_value)
        else:
            right_value = discount*valueGrid[right[0]][right[1]]
            right_reward = p_right*(rewardGrid[right[0]][right[1]] + right_value)
    
        if backward[0] < 0 or backward[0] >= len(valueGrid) or backward[1] < 0 or backward[1] >= len(valueGrid[0]) or backward in walls:
            backward_value = discount*valueGrid[currLoc[0]][currLoc[1]]
            backward_reward = p_backward*(wall_hit + backward_value)
        else:
            backward_value = discount*valueGrid[backward[0]][backward[1]]
            backward_reward = p_backward*(rewardGrid[backward[0]][backward[1]] + backward_value)
  
        if forward[0] < 0 or forward[0] >= len(valueGrid) or forward[1] < 0 or forward[1] >= len(valueGrid[0]) or forward in walls:
            forward_value = discount*valueGrid[currLoc[0]][currLoc[1]]
            forward_reward = p_forward*(wall_hit + forward_value)
        else:
            forward_value = discount*valueGrid[forward[0]][forward[1]]
            forward_reward = p_forward*(rewardGrid[forward[0]][forward[1]] + forward_value)
            

        total = left_reward + right_reward + backward_reward + forward_reward
        if total > currMax:
            currMax = total
            bestMove = currMove
    return (currMax,bestMove)

def calculate_theshold(config_file,newGrid,valueGrid):
    total = 0
    for y in range(len(valueGrid)):
        for x in range(len(valueGrid[0])):
            total += abs(newGrid[y][x] - valueGrid[y][x])
    if total < config_file["threshold_difference"]:
        return True
    else:
        return False

def mdp(config_file):
    map_size = config_file["map_size"]
    move_list = config_file["move_list"]
                
    valueGrid = initializeValue(config_file)
    rewards = initializeReward(config_file)
    policy = intializePolicy(config_file)
    pits = config_file["pits"]
    walls = config_file["walls"]
    goals = config_file["goals"]
    allPolicies = []
    print rewards
    for i in range(config_file["max_iterations"]):
#     for i in range(20):
        newGrid = copy.deepcopy(valueGrid)
        for y in range(len(valueGrid)):
            for x in range(len(valueGrid[0])):
                if [y,x] in pits or [y,x] in walls or [y,x] in goals:
                    continue
                else:
                    (value,movePolicy) = calcMaxValue(config_file,[y,x],valueGrid,rewards)
                    newGrid[y][x] = value
                    policy[y][x] = movePolicy
        curr_policy = []
        for rowPolicy in policy:
        	for move in rowPolicy:
        		curr_policy.append(move)
		allPolicies.append(curr_policy)

        if calculate_theshold(config_file,newGrid,valueGrid):
            valueGrid = newGrid
            print i
            break
        else:
            valueGrid = newGrid
        
#         tester = []
#         for y in range(1,len(valueGrid)-1):
#             hmm = []
#             for x in range(1,len(valueGrid[0])-1):
#                 hmm.append(valueGrid[y][x])
#             tester.append(hmm)
#         print tester

    print valueGrid
    return allPolicies
                    
                    

            
