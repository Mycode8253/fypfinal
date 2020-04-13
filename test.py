import tkinter

mycolor = '#%02x%02x%02x' % (64, 204, 208)  # set your favourite rgb color
mycolor2 = '#40E0D0'  # or use hex if you prefer 
root = tkinter.Tk()
root.configure(bg=mycolor)
tkinter.Button(root, text="Press me!", bg=mycolor, fg='black',
               activebackground='black', activeforeground=mycolor2).pack()
root.mainloop()