import tkinter as tk
import gurmatbibek


def test():
    print("test Passed!!")

root=tk.Tk()

height=700
width=800
canvas=tk.Canvas(root,height=height,width=width)
canvas.pack()

background=tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
backgroundLable=tk.Label(root, image=background)
backgroundLable.place(x=0,y=0,relheight=1,relwidth=1)

frame=tk.Frame(root,bg="#80c1ff")
frame.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

lable=tk.Label(frame,text="Enter a name of a topic \n(all options that include what you enter will show)")
lable.place(relx=0.3,rely=0,relwidth=0.45,relheight=0.25)

photo = tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
photo=photo.subsample(3,3)
button=tk.Button(frame,text="Search",bg="gray",command=test)#,image=photo)
button.place(relx=0.48,rely=0.4,relwidth=0.1,relheight=0.05)


entry=tk.Entry(frame)
entry.place(relx=0.4,rely=0.6,relwidth=0.25,relheight=0.1)


root.mainloop()