import tkinter as tk
import Image_test_Dyslexia
import learningtest 

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switchFrame(StartPage)
    

    def switchFrame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()
    
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        tk.Label(
            self ,
            text="Welcome to the test", 
            font =('Helvetica',18,"bold")).grid(
                row=0,
                column=1,
                ipady = 2,
            )
        tk.Button(
            self,
            text="Image Test",
            font=('Calibre',14,"italic"),
            command = lambda : master.switchFrame(Image_test_Dyslexia.ImageTestDyslexia)
    
            ).grid(
                row = 2,
                column =0,
                ipadx = 2,
                ipady =2, 
            )
        tk.Button(
            self,
            text="Learning Test",
            font=('Calibre',14,'italic'),
            command = lambda : master.switchFrame(learningtest.LearningTest)
            ).grid(
                row=2,
                column = 2,
                ipadx =2,

            )



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()