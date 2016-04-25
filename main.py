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


##Load Scripts
from Drone_int import * 
from myo_Input import *


active_myo=False 
active_drone=False

app_drone=Control()
#
def mens():

	pass
	#tkMessageBox.showinfo(title="Caution",message="Please , make sure that you're connected to \n  Red  wifi (Drone) \n  Bluetooth  connector MYO")
def ateb2():
	global lock_fly
	lock_fly.set(True)
	app_drone.ateb

def Emergency2():
	global lock_fly
	lock_fly.set(True)
	app_drone.Emergency

# Scale speed
def v_ver_speed(val):
	v_min=5.0
	v_max=100.0
	val=int(val)
	m1=(v_max-v_min)/(20.0)
	y1=m1*val -m1*5.0+v_min

	return y1

def v_rot_speed(val):
	v_min=5.0
	v_max=100.0
	val=int(val)
	m1=(v_max-v_min)/(190.0)
	y1=m1*val-m1*10.0+v_min

	return y1

#Init Myo
def connect_myo():
	print("Connecting to Myo ... Use CTRL^C to exit.")
	global active_myo
	try:
		global hub
		hub = libmyo.Hub()
		global App_myo
		App_myo=Listener()
		hub.set_locking_policy(libmyo.LockingPolicy.none)
		hub.run(1000, App_myo)
		time.sleep(1.5)
		if (App_myo.pair):
			active_myo=True
			tkMessageBox.showinfo(title="MYO",message="Connection OK")
		else:
			active_myo=False
			tkMessageBox.showerror(title="Error",message="Myo Hub could not be created. Make sure Myo Connect is running.")
			hub.shutdown()
	except:
		
		active_myo=False
		tkMessageBox.showerror(title="Error",message="Myo Hub could not be created. Make sure Myo Connect is running.")
		hub.shutdown()

#Init Drone
def connect_drone():
	global active_drone
	print ("Drone", active_drone)
	try :
		app_drone.dron_init()
		active_drone=True
		tkMessageBox.showinfo(title="Drone",message="Connection OK")
	except :
		tkMessageBox.showerror(title="Error",message="Drone not found. Make sure to connect the red wifi.")
		time.sleep(2)
		
		active_drone=False

	
	print ("myo ",active_myo)
	print ("Drone", active_drone)


def  proccesInput(app,drone,cycle_g2):
	"""
	Procces Input for the receiver data Myo and send to Drone

	"""
	takeoff=drone.takeoff_land
	myoRoll,myoPitch,myoYaw=CalculateRelativeEulerAngles (app.currentOrientation,app.referenceOrientation)
	myoRoll, myoPitch, myoYaw=RerangeEulerAngles (myoRoll, myoPitch, myoYaw)

	myoRoll, myoPitch, myoYaw=Filter_values(myoRoll, myoPitch, myoYaw)

	myoRoll=conver_grade(myoRoll)
	myoPitch=conver_grade(myoPitch)
	myoYaw=conver_grade(myoYaw)

	# #Condition for fly
	time_ret=0.08
	global info_myo


	if (takeoff and lock_fly.get()==False):
		if (app.pose==libmyo.Pose.fist ):
			droneRoll = float(myoPitch)
			dronePitch = float(-myoRoll)
			droneYaw = float(-myoYaw)
			drone.drone.update( cmd=movePCMDCmd( True, droneRoll, dronePitch, droneYaw, 0))
			info_myo.set("Fist")
			time.sleep(time_ret)
			drone.drone.hover()

		elif (app.pose==libmyo.Pose.fingers_spread):
			droneGaz = float(myoRoll)
			if (drone.drone.altitude>0.45):
				drone.drone.update( cmd=movePCMDCmd( True, 0, 0, 0, droneGaz))
				time.sleep(time_ret)
				drone.drone.hover()
			info_myo.set("Fingers Spread")

		elif (app.pose==libmyo.Pose.double_tap):
			drone.drone.takePicture()	
			info_myo.set("double Tap")

		elif (app.pose==libmyo.Pose.wave_in):
			global safe_land
			if(safe_land):
				print ("Land safe")
				safe_land=False
				global lock_fly
				lock_fly.set(True)
				drone.ateb()
			info_myo.set("Wave Right")
			if (last_pose==libmyo.Pose.double_tap or _last_pose==libmyo.Pose.double_tap ):

				safe_land=True
				print ("double tap + wave in ")

		elif (app.pose==libmyo.Pose.wave_out):
			info_myo.set("Wave Left")
			droneGaz = float(myoRoll)
			if (drone.drone.altitude>0.5):
				drone.drone.update( cmd=movePCMDCmd( True, 0, 0, 0, droneGaz))
				time.sleep(time_ret)
				drone.drone.hover()
		else:
			#
			info_myo.set("Rest")
			if (cycle_g2):
				#drone.drone.update( cmd=movePCMDCmd( True, 0, 0, 0,0))
				pass
				

	elif (app.pose==libmyo.Pose.wave_out):
		info_myo.set("Wave Left")
		if (last_pose==libmyo.Pose.double_tap or _last_pose==libmyo.Pose.double_tap and lock_fly.get()==False):
			drone.take_off_land()
			print ("Takeoff ")
	else:
		if (app.pose==libmyo.Pose.wave_in):
			info_myo.set("Wave Right")
		elif (app.pose==libmyo.Pose.fingers_spread):
			info_myo.set("Fingers Spread")
		elif (app.pose==libmyo.Pose.fist):
			info_myo.set("Fist ")
		elif (app.pose==libmyo.Pose.double_tap):
			info_myo.set("Double Tap")
		else: 
			info_myo.set("Rest...")

	if (app.myo_sync==False):
		info_myo.set("Unsynced")


	global last_pose
	global _last_pose
	if (last_pose != app.pose ):
		_last_pose=last_pose
		last_pose=app.pose
			
def batterylevel_drone(cycle):
	level= app_drone.drone.battery
	if (level<10 and cycle):
		tkMessageBox.showwarning(title="Warning",message="Drone \n Low battery...")
	global v_level_drone
	var=str(level)+"%"
	v_level_drone.set(var)

def batterylevel_myo(cycle):
	level= App_myo.level_battery
	if (level<5 and cycle):
		tkMessageBox.showwarning(title="Warning",message="Myo \n Low battery...")
	if (level <0.1):
		try :
			hub.shutdown()
		except:
			print ("Cannot do")
	global v_level_myo
	var=str(level)+"%"
	v_level_myo.set(var)


def url_v():
	webbrowser.open("https://github.com/Cubillosxy/MYO-PYTHON-BEBOP")


def main():

	"""
	GUI Programan 
	"""



	global last_pose
	last_pose=libmyo.Pose.rest
	global _last_pose
	_last_pose=libmyo.Pose.rest
	global safe_land
	safe_land=False
	global app_drone
	##GUI
	global raiz
	raiz=Tk()
	f1=Frame(raiz)

	##Settings
	l_setting=Label(f1,text="Settings",anchor="n",padx=2 )
	v_lineal=Scale(f1, from_=5, to=25, orient=HORIZONTAL,length=200, label= "Vertical Speed m/s x 10^-1" ,bg="white", tickinterval=10)
	v_lineal.set(10)
	v_angle=Scale(f1, from_=10, to=200, orient=HORIZONTAL,length=200, label= "Rotation Speed °/s " ,bg="white", tickinterval=95)
	v_angle.set(50)


	##side
	l_setting.pack(side=TOP)
	v_angle.pack()
	v_lineal.pack()
	x5_inicial=470
	f1.place(x=x5_inicial,y=5)

	#Level battery
	global v_level_myo 
	v_level_myo = StringVar(value="??")
	global v_level_drone
	v_level_drone=StringVar(value="??")
	txtleveldrone= Label(raiz, text="MYO",bg="white")   
	txtlevelmyo= Label(raiz, text="Drone",bg="white")  

	level_myo=Label(raiz, textvariable=v_level_myo, width=10,bg="white") 
	level_drone=Label(raiz, textvariable=v_level_drone, width=10,bg="white") 

	##image
	im_bat=PhotoImage(file="Bib_ima/bat1_57x44.gif")
	im_bat2=PhotoImage(file="Bib_ima/bat_57x44.gif")
	ima_bat=Label(raiz, image=im_bat, anchor="center",padx=2)
	ima_bat2=Label(raiz, image=im_bat2, anchor="center",padx=2)

	##
	
	y5_inicial=200
	txtleveldrone.place(x=x5_inicial,y=y5_inicial-8)
	txtlevelmyo.place(x=x5_inicial+106,y=y5_inicial-8)
	ima_bat.place(x=x5_inicial+40,y=y5_inicial-8)
	ima_bat2.place(x=x5_inicial+102+43,y=y5_inicial-8)
	level_myo.place(x=x5_inicial-20,y=y5_inicial-8+18)
	level_drone.place(x=x5_inicial-20+108,y=y5_inicial-8+18)

	#imagen drone
	raiz.title("MYO+PYTHON+BEBOP")
	raiz.geometry("690x550+300+70")

	raiz.configure(background='white')

	im_drone3 =PhotoImage(file="Bib_ima/bebop_420x145.ppm")
	im_drone = Label(raiz, image=im_drone3, anchor="center",padx=2)


	x1=800/2-420/2

	im_drone.place(x=20,y=12) 

	#load images
	zq1= PhotoImage(file='Bib_ima/cfp1_81x81.gif')
	ima_ade=PhotoImage(file='Bib_ima/cfp2_63x81a.gif')
	zq2=PhotoImage(file='Bib_ima/cfp3_81x81.gif')
	ima_izq=PhotoImage(file='Bib_ima/cfp4_81x63a.gif')
	zce=PhotoImage(file='Bib_ima/cfp5_63x63.gif')
	ima_der=PhotoImage(file='Bib_ima/cfp6_81x63a.gif')
	zq3=PhotoImage(file='Bib_ima/cfp7_81x81.gif')
	ima_aba=PhotoImage(file='Bib_ima/cfp8_63x81a.gif')
	zq4=PhotoImage(file='Bib_ima/cfp9_81x81.gif')


	### Joystick control primary

	botezq1=Label(raiz,image=zq1, anchor="center",padx=2)
	bot_ade=Button(raiz,image=ima_ade,command=lambda:app_drone.pitch_i(v_rot_speed(v_angle.get())))
	botezq2=Label(raiz,image=zq2, anchor="center",padx=2)
	bot_izq=Button(raiz,image=ima_izq,command=lambda:app_drone.roll_d(v_rot_speed(v_angle.get())))
	botezce=Button(raiz,image=zce,command=lambda:app_drone.center())
	bot_der=Button(raiz,image=ima_der,command=lambda:app_drone.roll_i(v_rot_speed(v_angle.get())))
	botezq3=Label(raiz,image=zq3, anchor="center",padx=2)
	bot_aba=Button(raiz,image=ima_aba, command=lambda:app_drone.pitch_d(v_rot_speed(v_angle.get())))
	botezq4=Label(raiz,image=zq4, anchor="center",padx=2)

	x_inicial=150
	y_inicio=280

	
	botezq1.place(x=x_inicial,y=y_inicio)
	bot_ade.place(x=x_inicial+81,y=y_inicio)
	botezq2.place(x=x_inicial+81+63,y=y_inicio)
	bot_izq.place(x=x_inicial,y=y_inicio+81)
	botezce.place(x=x_inicial+81,y=y_inicio+81)
	bot_der.place(x=x_inicial+81+63,y=y_inicio+81)
	botezq3.place(x=x_inicial,y=y_inicio+81+63)
	bot_aba.place(x=x_inicial+81,y=y_inicio+81+63)
	botezq4.place(x=x_inicial+81+63,y=y_inicio+81+63)

	### Joystick control secundary
	ima_gder=PhotoImage(file='Bib_ima/cfg1_81x81.ppm')
	ima_gizq=PhotoImage(file='Bib_ima/cfg2_81x81.ppm')
	ima_arr=PhotoImage(file='Bib_ima/cfar_81x81a.ppm')
	ima_down=PhotoImage(file='Bib_ima/cfab_81x81.ppm')


	
	bot_gder=Button(raiz,image=ima_gder,command=lambda:app_drone.yaw_d(v_rot_speed(v_angle.get())))
	bot_gizq=Button(raiz,image=ima_gizq,command=lambda:app_drone.yaw_i(v_rot_speed(v_angle.get())))
	bot_arr=Button(raiz,image=ima_arr,command=lambda:app_drone.gaz_su(v_ver_speed(v_lineal.get())))
	bot_dow=Button(raiz,image=ima_down,command=lambda:app_drone.gaz_ba(v_ver_speed(v_lineal.get())))



	x2_inicial=x_inicial+225+40
	y2_inicial=y_inicio-9   


	bot_gder.place(x=x2_inicial+81+81+2,y=y2_inicial+81)
	bot_arr.place(x=x2_inicial+81,y=y2_inicial-2)
	bot_gizq.place(x=x2_inicial-2,y=y2_inicial+81)
	bot_dow.place(x=x2_inicial+81,y=y2_inicial+81+81+2)


	##Buttons additionals
	ima_tkld=PhotoImage(file='Bib_ima/taklan_103x32.ppm')
	ima_land2=PhotoImage(file='Bib_ima/L2_81X32.ppm')
	ima_stop=PhotoImage(file='Bib_ima/stop_94x49.ppm')

	bot_tak_and =Button(raiz, image= ima_tkld, command=app_drone.take_off_land)  
	bot_lan_cont=Button(raiz, image=ima_land2, command=app_drone.ateb)  
	bot_stop=Button(raiz, image=ima_stop, command=app_drone.Emergency)  


	x3_inicial=x_inicial
	y3_inicial=y_inicio+20

	bot_tak_and.place(x=x3_inicial-130,y=y3_inicial)
	bot_lan_cont.place(x=x3_inicial-130+11,y=y3_inicial+65)
	bot_stop.place(x=x3_inicial-130+4,y=y3_inicial+130)



	##COPYRIGHT

	l_copyright=Label(raiz,text="COPYRIGHT (c) EDWIN CUBILLOS 2016",anchor="n",padx=2 ,bg="white")
	
	l_copyright.place(x=350-100,y=500-20+50)


	##MENU BAR

	barraMenu=Menu(raiz)
	
	mnuFile=Menu(barraMenu)
	mnuHelp=Menu(barraMenu)

	mnuFile.add_command(label='Exit',command=raiz.destroy)
	mnuHelp.add_command(label='Version', command= url_v)


	barraMenu.add_cascade(label="File",menu=mnuFile)
	barraMenu.add_cascade(label="Help",menu=mnuHelp)

	raiz.config(menu=barraMenu)

	#### Button connect

	ima_con_myo=PhotoImage(file='Bib_ima/conMyo_103x44.ppm')
	ima_con_drone=PhotoImage(file='Bib_ima/conDrone_103x44.ppm')
	
	bot_con_myo=Button(raiz,image=ima_con_myo,command=connect_myo)
	bot_con_drone=Button(raiz,image=ima_con_drone,command=connect_drone)

	y4_inicial=16+145+10
	x4_inicial=32+20

	bot_con_myo.place(x=x4_inicial,y=y4_inicial+4)
	bot_con_drone.place(x=x4_inicial+230,y=y4_inicial+4)

	#Check button
	global lock_fly
	lock_fly = BooleanVar() 
	idavue = Checkbutton(raiz, text='Lock Myo',variable=lock_fly,onvalue=True, offvalue=False)
	lock_fly.set(True)
	idavue.place(x=x4_inicial+130,y=y4_inicial+15)

	###Label for show info
	global info_myo 
	info_myo  = StringVar(value="No info")
	global info_drone
	info_drone=StringVar(value="No info")

	# txtleveldrone= Label(raiz, text="MYO",bg="white")   
	# txtlevelmyo= Label(raiz, text="Drone",bg="white")  

	label_info_myo=Label(raiz, textvariable=info_myo , width=50,bg="white") 
	label_info_drone=Label(raiz, textvariable=info_drone, width=50,bg="white") 

	label_info_myo.place(x=x4_inicial-120,y=y4_inicial+4+55)
	#label_info_drone.place(x=x4_inicial+230-120,y=y4_inicial+4+55)

	#optional msm 
	mens()
	

	flip=True
	
	cycle_g=False
	cycle_g2=False
	count=0
	count2=0
	limitc1=150000
	limitc2=8000
	#main loop
	try:
		while 1:	
			count +=1
			count2 +=1
			raiz.update_idletasks()
			raiz.update()
			if (count ==limitc1):
				cycle_g=True

			if (count2==limitc2):
				cycle_g2=True	
				

			if (active_myo):
				proccesInput(App_myo,app_drone,cycle_g2)
				#time.sleep(0.15)
				batterylevel_myo(cycle_g)
			
			if (active_drone):
				batterylevel_drone(cycle_g)
					
			# if (flip==True and active_drone==True):
			# 	print ("already for to fly", active_drone)
			# 	flip=False

			if (count ==limitc1):
				count=0
				cycle_g=False
			if (count2 ==limitc2):
				count2=0
				cycle_g2=False

	#for any error land and exit	
	except KeyboardInterrupt:
		print ("error")

	finally:
		#before to out 
		app_drone.ateb()
		try:		
			hub.shutdown()
		except:
			print ("Cannot do") 
		#exit()

if (__name__ == '__main__'):
	main()