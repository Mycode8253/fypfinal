import tkinter

mycolor = '#%02x%02x%02x' % (64, 204, 208)  # set your favourite rgb color
mycolor2 = '#40E0D0'  # or use hex if you prefer 
root = tkinter.Tk()
root.configure(bg=mycolor)
im_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\boat.png")
        im_1 = im_1.resize(SIZE,Image.ANTIALIAS)
        photo_1 = ImageTk.PhotoImage(im_1) 
button_1 = tk.Button(self, image = photo_1,command=lambda:threading.Thread(target=self.initRecognition,args=("boat"),daemon=True).start() )
        button_1.grid(row=3,column=5,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y)
root.mainloop()