import heapq
import copy

def astar(move_list,map_size,start_loc,goal_loc,walls,pits,cost):
    frontier = []
    
    board =  [[0 for i in range(map_size[1])] for j in range(map_size[0])]
    
    listOfMoves = []
    heapq.heappush(frontier,(0,[],start_loc))
    while True:
        node = heapq.heappop(frontier)
        currMoves = node[1]
        currLoc = node[2]
        for move in move_list:
            newMoves = copy.deepcopy(currMoves)
            possibleNew = [currLoc[0]+move[0],currLoc[1]+move[1]]
            if possibleNew in pits or possibleNew in walls:
                continue
            elif possibleNew[0] >= map_size[0] or possibleNew[1] >= map_size[1] or possibleNew[0] < 0 or possibleNew[1] < 0:
                continue
            elif possibleNew == goal_loc:
                newMoves.append(move)
                return convertToPath(start_loc,newMoves)
            else:
                newMoves.append(move)
                newV = calculate_heuristic(possibleNew,goal_loc) + (len(newMoves)*cost)
                heapq.heappush(frontier,(newV,newMoves,possibleNew))

def calculate_heuristic(curr_loc, goal_loc):
    return abs(curr_loc[0]-goal_loc[0]) + abs(curr_loc[1]-goal_loc[1]) 

def convertToPath(start,Moves):
    path = [start]
    currLoc = start;
    for move in Moves:
        newLoc = [currLoc[0]+move[0],currLoc[1]+move[1]]
        currLoc = newLoc
        path.append(newLoc)
    return path