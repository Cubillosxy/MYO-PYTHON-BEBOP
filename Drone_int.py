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

from core.bebop import *



class Control():
	"""
	Class for control proccess bebop
	"""
	def __init__(self):
		
		self.takeoff_land=False
		self.active=False
		self.d_time=0.1
		
		#self.dron_init()


	def dron_init(self):
		##drone
		self.drone=Bebop()
		self.speed=20
		self.active=not(self.active)
		

	def take_off_land(self):
		if (self.active):
			self.takeoff_land=not(self.takeoff_land)
			if (self.takeoff_land):
				print ("En el aire")
				self.takeoff()
			else:
				self.land()
				print ("Aterrizando")
		else:
			print ("Conectese al drone")


	
	def takeoff(self):
		self.drone.takeoff()
		time.sleep(1)
		print ("NOW FLAYING")
	
	# def fly_drone(self,roll,pitch,yaw,gaz):
	# 	if (self.takeoff_land):
	# 		self.drone.update( cmd=movePCMDCmd( True, roll, pitch, yaw , gaz ) )
			
	# 		print ("Vuela")
	# 	else:
	# 		print ("No ha despegado")


	def gaz_su(self,speed):
		if (self.takeoff_land):
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, 0 , speed ) )
			time.sleep(0.5)
			self.drone.trim()
			
			print ("subir ")
		else:
			print ("No ha despegado")

	def gaz_ba(self,speed):
		if (self.takeoff_land):
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, 0, -speed ) )
			time.sleep(self.d_time)
			self.drone.trim()
			

			print ("baja")
		else:
			print ("No ha despegado")

	def yaw_i(self,speed):
		if(self.takeoff_land):
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, -speed , 0 ) )
			time.sleep(self.d_time)
			self.drone.trim()

			print ("yaw izq")
		else:
			print ("No ha despegado")

	def yaw_d(self,speed):
		if(self.takeoff_land):
			self.drone.update( cmd=movePCMDCmd( True, 0, 0, speed , 0 ) )
			time.sleep(self.d_time)
			self.drone.trim()		
			print ("yaw der")
		else:
			print ("No ha despegado")

	def pitch_i(self,speed):
		if(self.takeoff_land):

			self.drone.update( cmd=movePCMDCmd( True, 0, speed, 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.trim()

			print ("pitch izq")
		else:
			print ("No ha despegado")

	def pitch_d(self,speed):
		if(self.takeoff_land):

			self.drone.update( cmd=movePCMDCmd( True, 0, -speed , 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.trim()

			print ("pitch der")
		else:

			print ("No ha despegado")

	def roll_i(self,speed):
		if(self.takeoff_land):

			self.drone.update( cmd=movePCMDCmd( True, speed , 0, 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.trim()

			print ("roll izq")
		else:
			print ("No ha despegado")

	def center(self):
		if(self.takeoff_land):
			self.drone.update( cmd=movePCMDCmd( True, 0 , 0, 0, 0 ) )
			print ("stop movement")
		else:
			print ("No ha despegado")

	def roll_d(self,speed):
		if(self.takeoff_land):
			self.drone.update( cmd=movePCMDCmd( True, -speed , 0, 0, 0 ) )
			time.sleep(self.d_time)
			self.drone.trim()

			print ("roll der")
		else:
			print ("No ha despegado")

	def ateb(self):
		if (self.takeoff_land):
			print ("aterrizaje controlado")
			self.drone.flyToAltitude(.5, timeout=20) 
			self.drone.land()
			self.takeoff_land=False
		else:
			print ("No esta en el aire")

	def Lande(self):
		self.drone.land()
		print ("aterrizaje de emergencia")

	def Emergency(self):
		print ("STOP EMERGENCY¡¡¡")
		if (self.takeoff_land):
			self.drone.emergency()
			print ("Emergency")



def main():


	mi_app = Control()

	mi_app.dron_init()


	print "aa"
	try:
		print (mi_app.drone.battery)
	except :
		pass
	print "ab"



 
if (__name__ == '__main__'):
    main()




















