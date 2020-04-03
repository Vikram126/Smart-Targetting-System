# Smart-Targetting-System
A Python-Arduino based Laser pointer system. 

requirements:
1.A pan-tilt module (Two servos : one for pan and another for tilt)
2.A laser diode
3.An IPcam or a Laptop camera
4.a microcontroller chip(I used an Arduino)

Working:
The turret is connected to the computer (wired/wireless). The user is prompted if he/she wants to use an IPcam or laptop camera.The turret should be placed accordingly. The camera streams images to the computer(If IPcam is selected, lower the stream quality to 320p for minimum lag). The python script detects a face and the coordinates are relayed to a special translation logic which converts coordinates on the image to angles. This data is later relayed to the microcontroller using this data structure: "X(x°)Y(y°)".
Eg. X45Y120.
The arduino code parses the data structure and relays them to the microcontroller.
