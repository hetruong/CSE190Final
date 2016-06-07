import random,math,sys,collections, operator
import copy, random

def convertStringToMove(move):
    #right
    if move == "E":
        return [0,1]
    #left
    elif move == "W":
        return [0,-1]
    #down
    elif move == "S":
        return [1,0]
    #up
    elif move == "N":
        return [-1,0]

def randomMove():
    chosen = random.randint(0,3)
    if chosen == 0:
        return "E"
    elif chosen == 1:
        return "W"
    elif chosen == 2:
        return "N"
    elif chosen == 3:
        return "S"


class QNode():
    
    def __init__(self,config_file):
        self.config_file = config_file
        self.values = {}
        self.used = collections.Counter();
        self.exit = False
        self.values["E"] = 0
        self.values["W"] = 0
        self.values["S"] = 0
        self.values["N"] = 0
        self.used["E"] = 0
        self.used["W"] = 0
        self.used["S"] = 0
        self.used["N"] = 0
        self.reward = 0
        
    def setQValue(self,action,value):
        self.values[action] = value;
        
    def getQValue(self,action):
        return self.values[action]
    
    def getMaxQValue(self):
        return max(self.values.values())
    
    def getMaxQAction(self):
#         print self.values
        return max(self.values.iteritems(), key=operator.itemgetter(1))[0]
    
    def getMaxAction(self):
        l_vals = {}
        for key,val in self.values.iteritems():
            if self.used[key] != 0:
                l_vals[key] = val + (self.config_file["explore_cnst"]/self.used[key])
            else:
                l_vals[key] = sys.maxint
        return max(l_vals.iteritems(), key=operator.itemgetter(1))[0]
    
    def getExitReward(self):
        return self.reward
    
    def setExitReward(self,newVal):
        self.reward = newVal;
        
    def updateCounter(self,move):
        self.used[move] += 1

class ReinforcementLearning():
    
    def __init__(self,config_file):
        self.config_file = config_file
        map_size = self.config_file["map_size"]

        random.seed(1)
        self.grid =  [[QNode(config_file) for i in range(map_size[1])] for j in range(map_size[0])]
        goals = self.config_file["goals"]    
        pits = self.config_file["pits"]
        self.epsilon = config_file["epsilon"]
        for goal in goals:     
            self.grid[goal[0]][goal[1]].exit = True
        for pit in pits:
            self.grid[pit[0]][pit[1]].exit = True
        self.QLearning()
        
    def randomPosition(self):
    	map_size = self.config_file["map_size"]
        pits = self.config_file["pits"]
        walls = self.config_file["walls"]
        goals = self.config_file["goals"]

        while True:
			y = random.randint(0,map_size[0]-1)
			x = random.randint(0,map_size[1]-1)
			if [y,x] not in pits and [y,x] not in walls and [y,x] not in goals:
				return [y,x]

    def QLearning(self):
		map_size = self.config_file["map_size"]    
		self.allPolicies = []
		self.epsilon = self.config_file["decrease_eps"]
		for i in range(1000):
			self.epsilon -= self.config_file["decrease_rate"]
			# print self.epsilon
			currPos = self.config_file["start"]
			# currPos = self.randomPosition()
			while True:
				if self.grid[currPos[0]][currPos[1]].exit:
					self.exitUpdate(currPos)
					break
				# currPos = self.QUpdateEpilson(currPos)
				currPos = self.QUpdate(currPos)
			print i
			currPolicy = self.printPolicy()
			self.allPolicies.append(currPolicy)
		# self.allPolicies = self.printPolicy()
		# self.allPolicies.append(curr_policy)


        # self.printLearnedValues()



    def exitUpdate(self,currPos):
        y = currPos[0]
        x = currPos[1]
        currQ = self.grid[y][x]
        alpha = self.config_file["learning_rate"]
        reward,actualPos = self.rewardFunction(currPos,currPos)
        newQVal = (1-alpha)*(currQ.getExitReward()) + (alpha*reward)
        currQ.setExitReward(reward)
        
        
    def QUpdateEpilson(self,currLoc):
        p_forward = self.config_file["prob_move_forward"]
        p_backward = self.config_file["prob_move_backward"]
        p_left = self.config_file["prob_move_left"]
        p_right = self.config_file["prob_move_right"]
        y = currLoc[0]
        x = currLoc[1]
        if random.random() < self.epsilon:
			# print "yoo"
			bestMove = randomMove()
        else:
            bestMove = self.grid[y][x].getMaxQAction() 
        move = convertStringToMove(bestMove)
        if move == [0,1]:
            left = [currLoc[0]-1,currLoc[1]]
            right = [currLoc[0]+1,currLoc[1]]
            backward = [currLoc[0],currLoc[1]-1]
            forward = [currLoc[0],currLoc[1]+1]            
        #left
        elif move == [0,-1]:
            left = [currLoc[0]+1,currLoc[1]]
            right = [currLoc[0]-1,currLoc[1]]
            backward = [currLoc[0],currLoc[1]+1]
            forward = [currLoc[0],currLoc[1]-1]
        #down
        elif move == [1,0]:
            left = [currLoc[0],currLoc[1]+1]
            right = [currLoc[0],currLoc[1]-1]
            backward = [currLoc[0]-1,currLoc[1]]
            forward = [currLoc[0]+1,currLoc[1]]
        #up
        elif move == [-1,0]:
            left = [currLoc[0],currLoc[1]-1]
            right = [currLoc[0],currLoc[1]+1]
            backward = [currLoc[0]+1,currLoc[1]]
            forward = [currLoc[0]-1,currLoc[1]]
            
        chosen = random.random()
        if chosen <= p_forward:
            newLoc = forward
        elif chosen <= (p_forward + p_backward):
            newLoc = backward
        elif chosen <= (p_forward + p_backward + p_left):
            newLoc = left
        else:
            newLoc = right
        
        reward,actualPos = self.rewardFunction(newLoc,currLoc)
        currQ = self.grid[y][x]
        newQ = self.grid[actualPos[0]][actualPos[1]]
        alpha = self.config_file["learning_rate"]
        beta = self.config_file["discount_factor"]
        newQVal = (1-alpha)*(currQ.getQValue(bestMove)) + (alpha)*(reward+(beta*newQ.getMaxQValue()))
        currQ.setQValue(bestMove,newQVal)
#         print actualPos
        return actualPos

    def QUpdate(self,currLoc):
        p_forward = self.config_file["prob_move_forward"]
        p_backward = self.config_file["prob_move_backward"]
        p_left = self.config_file["prob_move_left"]
        p_right = self.config_file["prob_move_right"]
        y = currLoc[0]
        x = currLoc[1]
        bestMove = self.grid[y][x].getMaxAction() 
        move = convertStringToMove(bestMove)
        if move == [0,1]:
            left = [currLoc[0]-1,currLoc[1]]
            right = [currLoc[0]+1,currLoc[1]]
            backward = [currLoc[0],currLoc[1]-1]
            forward = [currLoc[0],currLoc[1]+1]            
        #left
        elif move == [0,-1]:
            left = [currLoc[0]+1,currLoc[1]]
            right = [currLoc[0]-1,currLoc[1]]
            backward = [currLoc[0],currLoc[1]+1]
            forward = [currLoc[0],currLoc[1]-1]
        #down
        elif move == [1,0]:
            left = [currLoc[0],currLoc[1]+1]
            right = [currLoc[0],currLoc[1]-1]
            backward = [currLoc[0]-1,currLoc[1]]
            forward = [currLoc[0]+1,currLoc[1]]
        #up
        elif move == [-1,0]:
            left = [currLoc[0],currLoc[1]-1]
            right = [currLoc[0],currLoc[1]+1]
            backward = [currLoc[0]+1,currLoc[1]]
            forward = [currLoc[0]-1,currLoc[1]]
            
        chosen = random.random()
        if chosen <= p_forward:
            newLoc = forward
        elif chosen <= (p_forward + p_backward):
            newLoc = backward
        elif chosen <= (p_forward + p_backward + p_left):
            newLoc = left
        else:
            newLoc = right
        
        reward,actualPos = self.rewardFunction(newLoc,currLoc)
        currQ = self.grid[y][x]
        newQ = self.grid[actualPos[0]][actualPos[1]]
        alpha = self.config_file["learning_rate"]
        beta = self.config_file["discount_factor"]
        newQVal = (1-alpha)*(currQ.getQValue(bestMove)) + (alpha)*(reward+(beta*newQ.getMaxQValue()))
        currQ.updateCounter(bestMove)
        currQ.setQValue(bestMove,newQVal)
        return actualPos
        
    def rewardFunction(self,currLoc,oldLoc):
        pits = self.config_file["pits"]
        walls = self.config_file["walls"]
        goals = self.config_file["goals"]
        map_size = self.config_file["map_size"] 
        y = currLoc[0]
        x = currLoc[1]
        if currLoc in goals:
            reward = self.config_file["goal_rewards"][goals.index(currLoc)]
            # if reward >= 40.0:
            	# print reward
            return reward,currLoc
        elif currLoc in walls or y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[0]):
            return self.config_file["reward_for_hitting_wall"]+self.config_file["reward_for_each_step"],oldLoc
        elif currLoc in pits:
            return self.config_file["reward_for_falling_in_pit"],currLoc
        else:
            return self.config_file["reward_for_each_step"],currLoc
   

    def printLearnedValues(self):
        pits = self.config_file["pits"]
        goals = self.config_file["goals"]    
        walls = self.config_file["walls"]
        map_size = self.config_file["map_size"]
        vals =  [[0 for i in range(map_size[1])] for j in range(map_size[0])]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if [y,x] in goals or [y,x] in pits:
                    vals[y][x] = self.grid[y][x].getExitReward()
                elif [y,x] in walls:
                    vals[y][x] = self.config_file["reward_for_hitting_wall"]
                else:
                    vals[y][x] = self.grid[y][x].getMaxQValue() 
#                 print vals[y][x]
        print vals       
    
    def printPolicy(self):
        pits = self.config_file["pits"]
        goals = self.config_file["goals"]  
        walls = self.config_file["walls"]
        map_size = self.config_file["map_size"]
        policy =  [["" for i in range(map_size[1])] for j in range(map_size[0])]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
#                 print [y,x]
                if [y,x] in goals:
                    policy[y][x] = "GOAL"
                elif [y,x] in pits:
                    policy[y][x] = "PIT"
                elif [y,x] in walls:
                    policy[y][x] = "WALL"
                else:
                    policy[y][x] = self.grid[y][x].getMaxQAction() 
#                 print policy[y][x]
        # print policy
        curr_policy = []
        for rowPolicy in policy:
        	for move in rowPolicy:
        		curr_policy.append(move)
        return curr_policy