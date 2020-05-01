import tkinter as tk
import Image_test_Dyslexia
from PIL import Image, ImageTk
import learningtest 
import os
import wordusefluency
import evaluation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))
SIZE = (300, 300)
img_str=[]
number =1
global app
app=[]
class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.configure(self,background="#5CC7B2")
        tk.Tk.geometry(self,"1400x700")
        self.fullscreen=False
        self.frame = None
        self.switchFrame(StartPage)
        
    

    def switchFrame(self, frame_class,*awrgs,**kwargs):
        
        new_frame = frame_class(self,app)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()
    
class StartPage(tk.Frame):
    def __init__(self, master,strh):
        tk.Frame.__init__(self,master)
        tk.Frame.configure(self,bg="#5CC7B2")
     

        tk.Label(
            self,
            text="Dyslexia Screening Test", 
            font =('Times',24,"bold"),
            background="#5CC7B2").grid(
                row=0,
                column=1,
                pady = 2,
            )

        tk.Label(
            self,
            text="Hey there welcome to Test!",
            font=('Times',20,"normal"),
            background="#5CC7B2"
        ).grid(
            row=6,
            column=1,
            pady=4,
        )

        im_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\welcome.png")
        im_1 = im_1.resize(SIZE,Image.ANTIALIAS)
        img_str.append(ImageTk.PhotoImage(im_1))
        tk.Label(
            self,
            image=img_str[0],
            background="#5CC7B2",
        ).grid(
            row=7,
            column=1,
            pady=30
        )        
        tk.Label(
            self,
            text="We would like to know about your self a bit",
            font=('Times',18,"normal"),
            background="#5CC7B2",

        ).grid(
            row=8,
            column=1,
            pady=2
        )
        tk.Label(
            self,
            text="What is your age?",
            font=('Times',16,"normal"),
            background="#5CC7B2",

        ).grid(
            row=9,
            column=1,
            pady=4
        )
        e = tk.Entry(
            self,)
        e.grid(row=10,column=1,pady=10)
        tk.Button(
            self,
            text="Lets Start",
            font=("Times",15,"normal"),
            command= lambda: self.nextBtnFunction(e),
            relief = 'ridge'
        ).grid(
            row=11,
            column=1,
            pady=10,

        )

        

    
    def nextBtnFunction(self,e):
   
        if e.get()!="":
            app.switchFrame(evaluation.Evaluation)
        else:
                 tk.Label(
            self,
            text="You have not entered your age in the above box",
            font=('Helvitica',18,"bold"),
            background="red",

            ).grid(
            row=12,
            column=1,
            pady=4
            )

            
        # tk.Button(
        #     self,
        #     text="Image Test",
        #     font=('Calibre',14,"italic"),
        #     command = lambda : master.switchFrame(Image_test_Dyslexia.ImageTestDyslexia),
        #     relief = 'ridge'
        #     ).grid(
        #         row = 2,
        #         column =0,
        #         ipadx = 2,
        #         ipady =2, 
        #     )
        # tk.Button(
        #     self,
        #     text="Learning Test",
        #     font=('Calibre',14,'italic'),
        #     command = lambda : master.switchFrame(learningtest.LearningTest)
        #     ).grid(
        #         row=2,
        #         column = 2,
        #         ipadx =2,
        #         ipady =2, 

        #     )
        
        
        # tk.Button(
        #     self,
        #     text="Phenome Segmentation\n Test",
        #     font=('Calibre',14,'italic'),
        #     command = lambda : master.switchFrame(phenomeSeg.PhenomeSegmentation),
        #     relief = 'groove'
        #     ).grid(
        #         row=2,
        #         column = 4,
        #         ipadx =2,
        #         ipady =2,
        #     )
        
   

def quitFullScreen(event):
    if app.fullscreen:
        app.attributes("-fullscreen",False)
        app.fullscreen=False
    else: 
        app.attributes("-fullscreen",True)
        app.fullscreen=True


if __name__ == "__main__":

    app = MainWindow()
    app.bind("<Escape>",quitFullScreen)
    
    app.mainloop()

