#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016  Edwin Cubillos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



import math
import time
import sys
import struct
import signal
import six
import tkMessageBox
from Tkinter import *
import webbrowser
from core.bebop import *
import tkFont


class Control():
	"""
	Class for control proccess bebop
	"""
	def __init__(self):
		
		self.takeoff_land=False
		self.active=False
		self.d_time=0.3 #0.25
		self.info_drone="No connected"
		
		#self.dron_init()


	def dron_init(self):
		##drone
		self.drone=Bebop()
		self.speed=20
		self.active=not(self.active)
		self.info_drone="Ready to fly"
		

	def take_off_land(self):
		if (self.active):
			self.takeoff_land=not(self.takeoff_land)
			if (self.takeoff_land):
				self.takeoff()
			else:
				self.drone.land()
				print ("land...")
				self.info_drone="landing..."
				time.sleep(3)
		else:
			tkMessageBox.showinfo(title="Alert",message="Please connect to Drone ")

	def takeoff(self):
		self.drone.takeoff()
		self.info_drone="flying...."
		time.sleep(0.6)
		print ("NOW FLAYING")


	def gaz_su(self,speed):
		if (self.takeoff_land):
			self.info_drone="Up"
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, 0 , speed ) )
			time.sleep(self.d_time)
			self.drone.hover()
			print ("up")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def gaz_ba(self,speed):
		if (self.takeoff_land):
			self.info_drone="Down"

			if (self.drone.altitude>0.45):
				self.drone.update( cmd=movePCMDCmd( True, 0, 0, 0, -speed ) )
				time.sleep(self.d_time)
				self.drone.hover()
			

			print ("down")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def yaw_i(self,speed):
		if(self.takeoff_land):
			self.info_drone="Turn left"
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, -speed , 0 ) )
			time.sleep(self.d_time)
			self.drone.hover()

			print ("yaw left")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def yaw_d(self,speed):
		if(self.takeoff_land):
			self.info_drone="Turn Right"
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, speed , 0 ) )
			time.sleep(self.d_time)
			self.drone.hover()		
			print ("yaw right")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def pitch_i(self,speed):
		if(self.takeoff_land):
			self.info_drone="Forward"
			self.drone.update( cmd=movePCMDCmd( True, 0, speed, 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.hover()

			print ("pitch left")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def pitch_d(self,speed):
		if(self.takeoff_land):
			self.info_drone="Back"
			self.drone.update( cmd=movePCMDCmd( True, 0, -speed , 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.hover()

			print ("pitch right")
		else:

			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def roll_i(self,speed):
		if(self.takeoff_land):
			self.info_drone="Right"
			self.drone.update( cmd=movePCMDCmd( True, speed , 0, 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.hover()

			print ("roll left")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def center(self):
		if(self.takeoff_land):
			self.info_drone="Stop"
			self.drone.update( cmd=movePCMDCmd( True, 0 , 0, 0, 0 ) )
			#self.drone.hover
			print ("stop movement")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def roll_d(self,speed):
		if(self.takeoff_land):
			self.info_drone="Left"
			self.drone.update( cmd=movePCMDCmd( True, -speed , 0, 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.hover()

			print ("roll right")
		else:
			tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def ateb(self):
		if (self.takeoff_land):
			print ("Landing....")
			self.info_drone="Landing ++"
			self.drone.flyToAltitude(.75, timeout=17) 
			time.sleep(0.7)
			self.drone.land()
			self.takeoff_land=False
		else:
			pass
			#tkMessageBox.showinfo(title="Alert",message="Takeoff")

	def Lande(self):
		self.drone.land()
		print ("Landing....")

	def Emergency(self):
		
		if (self.takeoff_land):
			self.drone.emergency()
			self.info_drone="Stop Emergency"
			tkMessageBox.showinfo(title="Alert",message="Stop Emergency")
			time.sleep(3)
			



def main():


	mi_app = Control()

	mi_app.dron_init()
	try:
		print ("Level battery ",mi_app.drone.battery)
		while 1:
			
			print ("altitude", mi_app.drone.altitude)
	except KeyboardInterrupt :
		pass

 
if (__name__ == '__main__'):
    main()




















