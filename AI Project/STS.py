import tkinter as tk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import cv2
import PIL.Image, PIL.ImageTk
import time
import serial
import sys
#face detection using haar cascade classifier
faceCascade=cv2.CascadeClassifier(r"Face2.xml")

#arduino Connection
try:
#Change COM port and baud rate as per connections
    ard=serial.Serial('COM6',9600)
#let it connect
    time.sleep(2)
except Exception:
    print("Arduino not connected")
    sys.exit(0)
class Turret:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="Take a Picture", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.window.mainloop()
    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                       )
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.window.after(self.delay, self.update)



class MyVideoCapture:
    def __init__(self, video_source=0):
         # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
         # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #Scaling constants
        self.xScaleConst = (self.width) / 180;
        self.yScaleConst = (self.height) / 180;
         
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=faceCascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                    a,b=((x+w)/2)/self.xScaleConst, ((y+h)/2)/self.yScaleConst
                    message="X{0}:Y{1}".format(a,b)
                    ard.write(message,"utf8")
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
     # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
#to validate ip addresses
def validate_ip(s):
    a,b = s.split(':')
    a="".join(a).split(".")
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

root = tk.Tk()   # create a GUI window 
root.geometry("300x150") # set the configuration of GUI window 
root.title("Select Feed") # set the title of GUI window

def call(f_id):
    if f_id==1:
        root.destroy()
        Turret(tk.Tk(), "Turret")
    elif f_id==2:
        ip=sd.askstring("Enter IP address","https://",parent=root)
        if validate_ip(ip):
            ip="https://{}/video".format(ip)
            root.destroy()
            Turret(tk.Tk(), "Turret",ip)
        else:
            mb.showinfo("Error","Enter valid Ip")
            call(2)

# create a Form label 
tk.Label(text="Laptop Cam Or IP Webcam", bg="#90EE90", width="300", height="2", font=("Forte", 13)).pack() 
tk.Label(text="").pack() 

p=[tk.PhotoImage(file=r"Icons\laptop.png"),tk.PhotoImage(file=r"Icons\cctv.png")]
q=[l.subsample(10,10) for l in p]

b1=tk.Button(root,text="Laptop Cam",command=lambda : call(1),image=q[0],compound=tk.TOP).pack(padx=50,pady=5,side=tk.LEFT)
b2=tk.Button(root,text='IP Webcam',command=lambda : call(2),image=q[1],compound=tk.TOP).pack(padx=2,pady=5,side=tk.LEFT) 
root.mainloop() # start the GUI
