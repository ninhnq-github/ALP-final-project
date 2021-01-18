import cv2 
import numpy as np

def test():
    url = 'http://192.168.0.101:8080/video'
    cap = cv2.VideoCapture(url)
    while(True):
        ret, frame = cap.read()
        frame = cv2.resize(frame,(1000,int(1000/frame.shape[1]*frame.shape[0])))
        if frame is not None:
            cv2.imshow('frame',frame)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break
    cv2.destroyAllWindows()


def getCameraStream(url):
    try:
        cap = cv2.VideoCapture(url)
        return True, cap
    except:
        return False, None
    

from tkinter import *
from PIL import ImageTk, Image
import cv2


#root = Tk()
# Create a frame
#app = Frame(root, bg="white")
#app.grid()
# Create a label in the frame
#lmain = Label(app)
#lmain.grid()

# Capture from camera
#cap = cv2.VideoCapture(0)

# function for video streaming
def video_stream(lmain, cap):
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(cv2image,(400,300))
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream, lmain, cap) 

#video_stream(lmain,cap)
#root.mainloop()