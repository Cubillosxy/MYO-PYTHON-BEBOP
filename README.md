<p align="center" >  <h1>MYO+PYTHON+BEBOP </h1> </p>
=========


Program developed for fly drone bebop, it integrate the Myo armband and Bebop drone on python, also you can fly with buttons


For detail info see
https://github.com/Cubillosxy/MYO-PYTHON-BEBOP
<p align="center">
[MYO-PYTHON-DRONE](https://github.com/Cubillosxy/MYO-PYTHON-BEBOP/blob/master/Bib_ima/image_s.jpg)
</p>

# Notes

This  project is *work in progress* and it is your responsibility if you decide to use it without understanding the risks.
Inspiration and message codes are taken from official Parrot SDK:
https://github.com/ARDroneSDK3

Requirements:
* Python 2.X 
* Myo library
* Myo Connect

That project uses:

<p>[https://github.com/robotika/katarina/]   library for control of bebop </p>
<p>[https://github.com/NiklasRosenstein/myo-python]	 library for control of Myo </p>



Actually only you can fly, the video stream is not supported.

_Warning!_ this project uses libraries who still is on developing , then you can experimenter different problems
I recommend restart the program for any problem, if the issue continue reconnect all the devices.

The code evolved into next files:

* _main.py_     this is the main file who import other control files, this file contains the GUI, 
* _Drone_Int.py_  here you can find some functions for fly drone.
* _myo_Input.py_  this file contains the main functions for send and receiver data for myo, also contain functions for data procesing 

Known bugs:
* Wifi drone only support one connection, for avoid problems only connect your PC to Wifi drone


<h3>Thanks to: </h3>
* NiklasRosenstein  for myo-python library: [myo-python](https://github.com/NiklasRosenstein/myo-python)
* Group of robotika.cz for katarina		  : [katarina](https://github.com/robotika/katarina)
* Aldo Contreras González for contribution: aldocontrego@gmail.com



#Questions?

Edwin Cubillos Bohorquez, Colombia : edwin.cubillos@uptc.edu.co
----
<p align="center">This project is licensed under the MIT License.</br>
Copyright  2016 Edwin Cubillos</p>






