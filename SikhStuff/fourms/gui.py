import tkinter as tk
from tkinter import font




def test():
    print("test Passed!!")

root=tk.Tk()

height=700
width=800
canvas=tk.Canvas(root,height=height,width=width)
canvas.pack()

background=tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
#backgroundLable=tk.Label(root, image=background)
#backgroundLable.place(x=0,y=0,relheight=1,relwidth=1)

frame=tk.Frame(root,bg="#80c1ff")
frame.place(relx=0,rely=0,relwidth=1,relheight=1)

instruction=tk.Label(frame,font=("courier",11),text="Enter a name of a topic OR a name of a Gursikh.\n(When you type in the search box, the program will go through the\n Gurmat Bibek, Tapoban and Sikh Unity WordPress sites \nand search through the fourms.\n You can type the username of Gursikhs who posted Gurmat bibek and get back all \nthe fourms started by that person.")
instruction.place(relx=0.05,rely=0,relwidth=0.9,relheight=0.2)


entry=tk.Entry(frame)
entry.place(relx=0.3,rely=0.2,relwidth=0.25,relheight=0.1)

#photo = tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
#photo=photo.subsample(3,3)

guiFourms.forGui=[]
button=tk.Button(frame,font=("courier",12),text="Search",bg="gray",command=lambda: guiFourms.main(entry.get()))
button.place(relx=0.4,rely=0.3,relwidth=0.1,relheight=0.05)


lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.37, rely=0.4, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame,font=("courier",18))
label.place(relwidth=1, relheight=1)

if label["text"]!="":
    numbutton=tk.Button(frame,font=("courier",12),text="num",bg="gray",command=test)
    numbutton.place(relx=0.4,rely=0.3,relwidth=0.1,relheight=0.05) 
#print(tk.font.families())
root.mainloop()
print(guiFourms.forGui)