# importing only those functions 
# which are needed 
import  tkinter as tk
import tkinter.ttk as ttk
from PIL import Image,ImageTk
from backend import *
import os

SIZE = (300,300)
PADDING_IMAGE_X = 5
PADDING_IMAGE_Y = 5
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))





# creating tkinter window 
root = tk.Tk() 

# Adding widgets to the root window 
tk.Label(root, text = 'Learning Disability', font =( 
'Verdana', 15)).grid(row=0,column=3)

# Creating a photoimage object to use image 


im_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\boat.png")
im_1 = im_1.resize(SIZE,Image.ANTIALIAS)
photo_1 = ImageTk.PhotoImage(im_1) 

im_2 = Image.open(BASE_DIR+"\\tinkerpro\\img\\car.png")
im_2 = im_2.resize(SIZE,Image.ANTIALIAS)
photo_2 = ImageTk.PhotoImage(im_2) 

im_3 = Image.open(BASE_DIR+"\\tinkerpro\\img\\computer.png")
im_3 = im_3.resize(SIZE,Image.ANTIALIAS)
photo_3 = ImageTk.PhotoImage(im_3) 


im_4 = Image.open(BASE_DIR+"\\tinkerpro\\img\\windmill.png")
im_4 = im_4.resize(SIZE,Image.ANTIALIAS)
photo_4 = ImageTk.PhotoImage(im_4) 
# here, image option is used to 
# set image on button 
button_1 = tk.Button(root, image = photo_1,command=lambda: initRecognition("boat"))
button_1.grid(row=3,column=5,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 
button_2 = tk.Button(root, image = photo_2,command=lambda: initRecognition("car"))
button_2.grid(row=3,column=6,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 
button_3 = tk.Button(root, image = photo_3,command=lambda: initRecognition("computer"))
button_3.grid(row=4,column=5,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 
button_4 = tk.Button(root, image = photo_4,command=lambda: initRecognition("windmill"))
button_4.grid(row=4,column=6,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 

Question = tk.Label(root,font=('Helvetica', '14'),text="Hello, \nSelect the picture that represents a car ?")
Question.grid(row=2,column = 0,sticky=tk.W,padx = 20,pady=20)



tk.mainloop() 
