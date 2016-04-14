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

#
def mens():
	pass
	#tkMessageBox.showinfo(title="Caution",message="Please , make sure that you're connected to \n  Red  wifi (Drone) \n  Bluetooth  connector MYO")
	
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
		hub.run(100, App_myo)
		
		active_myo=True

	except MemoryError:
		print("Myo Hub could not be created. Make sure Myo Connect is running.")
	except:
		
		active_myo=False
		tkMessageBox.showinfo(title="Error",message="Myo Hub could not be created. Make sure Myo Connect is running.")

#Init Drone
def connect_drone():
	global active_drone
	print ("Drone", active_drone)
	try :
		app_drone.dron_init()
		active_drone=True
		
	except :
		tkMessageBox.showinfo(title="Error",message="Drone not found. Make sure to connect the red wifi.")
		time.sleep(2)
		
		active_drone=False

	
	print ("myo ",active_myo)
	print ("Drone", active_drone)

		

def  proccesInput(app,drone):
	"""
	Procces Input for the receiver data Myo and send to Drone

	"""
	takeoff=drone.takeoff_land
	myoRoll,myoPitch,myoYaw=CalculateRelativeEulerAngles (app.currentOrientation,app.referenceOrientation)
	myoRoll, myoPitch, myoYaw=RerangeEulerAngles (myoRoll, myoPitch, myoYaw)

	myoRoll=conver_grade(myoRoll)
	myoPitch=conver_grade(myoPitch)
	myoYaw=conver_grade(myoYaw)

	# #Condition for fly
	if (takeoff):
		if (app.pose==libmyo.Pose.fist ):
			droneRoll = float(-myoPitch)
			dronePitch = float(myoRoll)
			droneYaw = float(-myoYaw)
			drone.drone.update( cmd=movePCMDCmd( True, droneRoll, dronePitch, droneYaw, 0))
			
		elif (app.pose==libmyo.Pose.fingers_spread):
			droneGaz = float(myoPitch)
			drone.drone.update( cmd=movePCMDCmd( True, 0, 0, 0, droneGaz))

		elif (app.pose==libmyo.Pose.double_tap):
			drone.drone.takePicture()				
		elif (app.pose==libmyo.Pose.rest):
			drone.drone.update( cmd=movePCMDCmd( True, 0, 0, 0, 0) )
			
def batterylevel():
	level= app_drone.drone.battery

def conver_grade(angle):
    angle= (angle*180.0)/math.pi
    return angle

def url_v():
	webbrowser.open("https://github.com/Cubillosxy/MYO-PYTHON-BEBOP")


def main():

	"""
	GUI Programan 
	"""

	global app_drone
	app_drone=Control()

	##GUI
	global raiz
	raiz=Tk()
	f1=Frame(raiz)

	##Settings
	l_setting=Label(f1,text="Settings",anchor="n",padx=2 )
	v_lineal=Scale(f1, from_=5, to=25, orient=HORIZONTAL,length=200, label= "Vertical Speed m/s x 10^-1" ,bg="white", tickinterval=10)
	v_lineal.set(1)
	v_angle=Scale(f1, from_=10, to=200, orient=HORIZONTAL,length=200, label= "Rotation Speed °/s " ,bg="white", tickinterval=95)
	v_angle.set(50)


	##side
	l_setting.pack(side=TOP)
	v_angle.pack()
	v_lineal.pack()

	f1.place(x=450,y=5)

	raiz.title("MYO+PYTHON+BEBOP")
	raiz.geometry("680x550+300+70")

	raiz.configure(background='white')

	im_drone3 =PhotoImage(file="Bib_ima/bebop_420x145.gif")
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
	ima_gder=PhotoImage(file='Bib_ima/cfg1_81x81.gif')
	ima_gizq=PhotoImage(file='Bib_ima/cfg2_81x81.gif')
	ima_arr=PhotoImage(file='Bib_ima/cfar_81x81a.gif')
	ima_down=PhotoImage(file='Bib_ima/cfab_81x81.gif')


	
	bot_gder=Button(raiz,image=ima_gder,command=lambda:app_drone.yaw_d(v_rot_speed(v_angle.get())))
	bot_gizq=Button(raiz,image=ima_gizq,command=lambda:app_drone.yaw_i(v_rot_speed(v_angle.get())))
	bot_arr=Button(raiz,image=ima_arr,command=lambda:app_drone.gaz_su(v_ver_speed(v_lineal.get())))
	bot_dow=Button(raiz,image=ima_down,command=lambda:app_drone.gaz_ba(v_ver_speed(v_lineal.get())))



	x2_inicial=x_inicial+225+30
	y2_inicial=y_inicio-9   


	bot_gder.place(x=x2_inicial+81+81+2,y=y2_inicial+81)
	bot_arr.place(x=x2_inicial+81,y=y2_inicial-2)
	bot_gizq.place(x=x2_inicial-2,y=y2_inicial+81)
	bot_dow.place(x=x2_inicial+81,y=y2_inicial+81+81+2)


	##Buttons additionals
	ima_tkld=PhotoImage(file='Bib_ima/taklan_103x32.gif')
	ima_land2=PhotoImage(file='Bib_ima/L2_81X32.gif')
	ima_stop=PhotoImage(file='Bib_ima/stop_94x49.gif')

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

	ima_con_myo=PhotoImage(file='Bib_ima/conMyo_103x44.gif')
	ima_con_drone=PhotoImage(file='Bib_ima/conDrone_103x44.gif')
	
	bot_con_myo=Button(raiz,image=ima_con_myo,command=connect_myo)
	bot_con_drone=Button(raiz,image=ima_con_drone,command=connect_drone)

	y4_inicial=16+145 
	x4_inicial=32+20

	bot_con_myo.place(x=x4_inicial,y=y4_inicial+4)
	bot_con_drone.place(x=x4_inicial+230,y=y4_inicial+4)


	#optional msm 
	mens()
	

	flip=True
	count=0


	#main loop
	while 1:
		count +=1
		try:
			
			raiz.update_idletasks()
			raiz.update()
			
			if (active_myo):
				proccesInput(App_myo,app_drone)
				time.sleep(0.15)

			
			if (active_drone):
				batterylevel()
				if (count ==1000):
					count=0
					app_drone.center()
		#for any error land and exit	
		except :
			print ("exp")
			app_drone.ateb()
			exit()

		if (flip==True and active_drone==True):
			print ("already for to fly", active_drone)
			flip=False
		

	

if (__name__ == '__main__'):
	main()