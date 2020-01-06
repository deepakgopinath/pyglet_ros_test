#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Joy
from envs.envs import SimpleHA2D
from simple_ha2d.msg import CartVelCmd
import numpy as np

class Simulator(object):
	"""docstring for Simulator"""
	def __init__(self, dim):
		super(Simulator, self).__init__()
		rospy.init_node("Simulator")
		rospy.on_shutdown(self.shutdown_hook)
		rospy.Subscriber('/joy', Joy, self.joy_callback)
		self.env = SimpleHA2D(2)
		self.dim = dim
		if rospy.has_param('max_cart_vel'):
			self._max_cart_vel = np.array(rospy.get_param('max_cart_vel'))
		else:
			self._max_cart_vel = 0.25*np.ones(self.dim)
			rospy.logwarn('No rosparam for max_cart_vel found...Defaulting to max linear velocity of 50 cm/s and max rotational velocity of 50 degrees/s')

		r = rospy.Rate(10)
		isStart = True
		self.env.run()
		
		# while not rospy.is_shutdown():
		# 	print "H"
		# 	#update human robot and autonomy actions

		# 	#simulate physics

		# 	#render to screen

		# 	if isStart:

		# 		isStart = False
		# 	r.sleep()

	def joy_callback(self, msg):
		_axes = np.array(msg.axes)
		for i in range(self.dim):
			self.user_vel.velocity.data[i] = 0.0

		self.user_vel.velocity.data[0] = -_axes[0] * self._max_cart_vel[0]
		self.user_vel.velocity.data[1] = -_axes[1] * self._max_cart_vel[1]
		self.user_vel.header.stamp = rospy.Time.now()
		self.env.update_human_velocity(self.user_vel)

	def shutdown_hook(self):
		pass
if __name__ == '__main__':
	Simulator(2)
	rospy.spin()