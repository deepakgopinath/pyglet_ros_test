#!/usr/bin/env python
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2Random, b2CircleShape, b2Vec2)
import rospy
from backends.framework import (Framework, Keys)
from IPython import embed

class Robot(object):
	def __init__(self, world, position, radius=3, type='kinematic'):
		if type == 'kinematic':
			self.robot = world.CreateKinematicBody(
	            position=position,
	            shapes=[b2CircleShape(pos=position, radius=radius)]
			)

		#TODO add else with creation of dynamic body


	def update(self, velocity):
		self.robot.linearVelocity = velocity

class Goal(object):
	def __init__(self, world, position, radius):
		self.static_goal = world.CreateStaticBody(
            position=position,
            shapes=[b2CircleShape(pos=position, radius=radius)] #change this to circles
		)

	def update(self):
		pass

class SimpleHA2D(Framework):
	#SimpleHA2D is a subclass of PygletFramework which is in turn a subclass of FrameworkBase
	name = "SimpleHA2D"
	description = '2D environment for human autonomy point robots'
	def __init__(self, num_goals):
		super(SimpleHA2D, self).__init__()
		self.world.gravity = (0,0) #So that this is a flat 2D world with no grvity.
		self.num_goals = num_goals
		self.autonomy_goals = []
		self.human_goals = []
		self.autonomy_velocity = b2Vec2(0.0, 0.0)
		self.human_velocity = b2Vec2(0.0, 0.0)

		ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=[b2EdgeShape(vertices=[(0, 35), (0, -35)])]
		)

		self.autonomy_robot = Robot(self.world, position=(5,9), radius=1)
		self.human_robot = Robot(self.world, position=(-5,9), radius=1)
        # self.body = self.world.CreateDynamicBody(position=(10,0))


	def update_human_velocity(self, human_velocity):
		self.human_velocity.x = human_velocity.velocity.data[0]
		self.human_velocity.y = human_velocity.velocity.data[1]

	def update_autonomy_velocity(self, autonomy_velocity):
		self.autonomy_velocity.x = autonomy_velocity.velocity.data[0]
		self.autonomy_velocity.y = autonomy_velocity.velocity.data[1]

	def Step(self, settings):
		self.autonomy_robot.update(self.autonomy_velocity)
		self.human_robot.update(self.human_velocity)
		super(SimpleHA2D, self).Step(settings)


class ComplexHA2D(Framework):
	#ComplexHA2D is a subclass of PygletFramework which is in turn a subclass of FrameworkBase
	name = "Bullet"
	description = 'A test for very fast moving objects (bullets)'
	def __init__(self):
		super(ComplexHA2D, self).__init__()

	def Step(self):
		pass
