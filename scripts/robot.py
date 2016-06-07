#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool
from cse_190_assi_3.msg import AStarPath, PolicyList
from read_config import read_config
from astar import astar
from mdp import mdp
from qlearning import ReinforcementLearning

#robot.py implementation goes here
class Robot():
	def __init__(self):
		self.config = read_config()
		self.finished_pub = rospy.Publisher("/map_node/sim_complete", Bool ,queue_size=20)
		self.path_list = rospy.Publisher("/results/path_list", AStarPath ,queue_size=30)
		self.policy_list = rospy.Publisher("/results/policy_list", PolicyList ,queue_size=100)
		rospy.init_node('robot',anonymous=True)
		self.rate = rospy.Rate(1)
		rospy.sleep(1)
		# move_list = self.config["move_list"]
		# map_size = self.config["map_size"]
		# start = self.config["start"]
		# goal = self.config["goal"]
		# walls = self.config["walls"]
		# pits = self.config["pits"]
		# cost = self.config["reward_for_each_step"]
		# a_star = astar(move_list,map_size,start,goal,walls,pits,cost)
		# mdp_policies = mdp(self.config)
		reinforcement = ReinforcementLearning(self.config)
		# # for move in a_star:
		# # 	self.path_list.publish(move)
		# rospy.sleep(1)
		# for policy in mdp_policies:
			# self.policy_list.publish(mdp_policies[len(mdp_policies)-1])
		for i in range(1000):
			self.policy_list.publish(reinforcement.allPolicies[999])
			# rospy.sleep(1)
			
		rospy.sleep(1)
		self.finished_pub.publish(True)
		rospy.sleep(1)
		rospy.signal_shutdown("finished moving")

if __name__ == '__main__':
	r = Robot()