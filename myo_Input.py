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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myo as libmyo; libmyo.init()
import time
import sys
import math

class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.02  # Output only 0.05 seconds

    def __init__(self):
        super(Listener, self).__init__()
        self.orientation = None
        self.pose = libmyo.Pose.rest
        self.emg_enabled = False
        self.locked = False
        self.rssi = None
        self.emg = None
        self.last_time = 0
        self.currentOrientation=[0,0,0,0]
        self.referenceOrientation=[0,0,0,0]
        self.level_battery=0


        ##Data vector
        self.num_data=3
        list1=[0]*4
        self.v_Orientation=[]
        for i in range( self.num_data) :
            self.v_Orientation.append(list1)




    def on_connect(self, myo, timestamp, firmware_version):
        myo.vibrate('short')
        myo.request_rssi()
        myo.request_battery_level()


    def on_pose(self, myo, timestamp, pose):
        if (pose == libmyo.Pose.fingers_spread or pose==libmyo.Pose.fist):
            self.referenceOrientation=self.currentOrientation

        self.pose = pose


    def on_orientation_data(self, myo, timestamp,quat):
        
        self.currentOrientation=[quat.x, quat.y, quat.z, quat.w]
       

    def on_unlock(self, myo, timestamp):
        self.locked = False
        

    def on_lock(self, myo, timestamp):
        self.locked = True
        


    def on_pair(self, myo, timestamp, firmware_version):
        print("Hello, Myo!")
        """
        Called when a Myo armband is paired.
        """

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """
        print("Bye Myo")

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation,
                    warmup_state):
        print("Sincronizad")

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """
        print("Sinn Sincronizad")

    def on_battery_level_received(self, myo, timestamp, level):
        """
        Called when the requested battery level received.

        """
        self.level_battery=level
        


def CalculateRelativeAngle(current, reference ):
    """
    Calculate one relative angle between the current angle and the reference angle
    """


    ## Because our domain is circular (-PI and +PI are the same) we calculate
    # the smallest difference and return 

    angle = current - reference

    if (angle > math.pi):
        return angle - 2*math.pi
        
    if (angle < -math.pi):
        return angle + 2*math.pi
        
    return angle;


    # diff1 = current - 2 * math.pi - reference
    # diff2 = current - reference
    # diff3 = current + 2 * math.pi - reference
    

        

    # abs1 = abs(diff1) #*1e
    # abs2 = abs(diff2) #*1e
    # abs3 = abs(diff3) #*1e

    # min1 = min(abs1, min(abs2, abs3))
    
   

    # if (min1 == abs1):
    #     return diff1
    # if (min1 == abs3):
    #     return diff3
    # else:
    #     return diff2





def CalculateAnglesm(quat):
    """
    calculate ROLL, PITCH and YAW
    """

    x, y, z, w = quat[0], quat[1], quat[2], quat[3]
        
    roll = math.atan2(2.0*y*w - 2.0*x*z, 1.0 - 2.0*y*y - 2.0*z*z)
    pitch = math.atan2(2.0*x*w - 2.0*y*z, 1.0 - 2.0*x*x - 2.0*z*z)
    yaw = math.asin(2.0*x*y + 2.0*z*w)    
    return roll,pitch,yaw



def RerangeEulerAngle(angle,deadzone,max):

    """
        Rerange the angles to [-1 - +1]
        If one angle is in the deadzone it is set to 0
        Angles are cubed for better control
        Deadzone and max is configurable 

    """
   
    sign=math.copysign(1, angle)


    value = abs(angle)

    if (value < deadzone):
        
        angle = 0
        return angle
        
    else:
        
            # current range of value: [deadzone - inifinite]
        value = float(min(value, max))
            #current range of value: [deadzone - max]
        value -= deadzone
            #current range of value: [0 - (max - deadzone)]
        value /= (max - deadzone)
            #current range of value: [0 - 1]

        #angle = float(sign* pow(value, 3))
        angle = float(sign*value)
    return angle 


def RerangeEulerAngles(roll,pitch,yaw):

    """

       
         Rerange the angles to [-1 - +1]
         If one angle is in the deadzone it is set to 0
         Angles are cubed for better control
         Deadzone and max is configurable 

    """
    
    # dead Zona  
    rollDeadzone = 0.16
    pitchDeadzone = 0.25
    yawDeadzone = 0.16

    rollMax = 0.38              #.35 st
    pitchMax = 0.38
    yawMax = 0.38

    roll= RerangeEulerAngle(roll,rollDeadzone,rollMax)
    pitch=RerangeEulerAngle(pitch, pitchDeadzone, pitchMax)
    yaw= RerangeEulerAngle(yaw, yawDeadzone, yawMax)

    return (roll,pitch,yaw)


def CalculateRelativeEulerAngles(currentOrientation,referenceOrientation):

    """

     Calculate all relative angles between the current orientation and the reference orientation

    """
    currentRoll,currentPitch,currentYaw = CalculateAnglesm (currentOrientation)
    referenceRoll, referencePitch, referenceYaw=CalculateAnglesm (referenceOrientation)
    roll = CalculateRelativeAngle(currentRoll, referenceRoll)
    pitch = CalculateRelativeAngle(currentPitch, referencePitch)
    yaw = CalculateRelativeAngle(currentYaw, referenceYaw)
    return roll,pitch,yaw


def conver_grade(angle):
    angle= (angle*180.0)/math.pi

    return angle


def  proccesOutRobotEdw(app):
    myoRoll,myoPitch,myoYaw=CalculateRelativeEulerAngles (app.currentOrientation,app.referenceOrientation)
    
    myoRoll1, myoPitch1, myoYaw1=RerangeEulerAngles (myoRoll, myoPitch, myoYaw)

    currentRoll,currentPitch,currentYaw = CalculateAnglesm (app.currentOrientation)
    referenceRoll, referencePitch, referenceYaw=CalculateAnglesm (app.referenceOrientation)

    if (app.pose==libmyo.Pose.fist):
        print ("sin Rerange")
        print ("roll ", myoRoll,"pitch ", myoPitch,"yaw", myoYaw)
        print ("roll ", conver_grade(myoRoll),"pitch ", conver_grade(myoPitch),"yaw", conver_grade(myoYaw))
        

    elif (app.pose==libmyo.Pose.fingers_spread):
        print ("con range")
        print ("roll ",  myoRoll1,"pitch ", myoPitch1,"yaw", myoYaw1)
        print ("roll ", conver_grade(myoRoll1),"pitch ", conver_grade(myoPitch1),"yaw", conver_grade(myoYaw1))
    elif (app.pose==libmyo.Pose.double_tap):
        pass
        


def main():
    print("Connecting to Myo ... Use CTRL^C to exit.")
    try:
        hub = libmyo.Hub()
    except MemoryError:
        print("Myo Hub could not be created. Make sure Myo Connect is running.")
        return
    myApp=Listener()
    hub.set_locking_policy(libmyo.LockingPolicy.none)
    hub.run(1, myApp)

    # Listen to keyboard interrupts and stop the hub in that case.
    try:
        while hub.running:
            time.sleep(0.25)
            proccesOutRobotEdw (myApp)
    except KeyboardInterrupt:
        print("\nQuitting ...")
    finally:
        print("Shutting down hub...")
        hub.shutdown()


if __name__ == '__main__':
    main()
  
