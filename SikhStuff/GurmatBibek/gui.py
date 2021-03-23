import tkinter as tk

height=700
width=800

root=tk.Tk()

canvas=tk.Canvas(root,height=height,width=width)
canvas.pack()

frame=tk.Frame(root,bg="#80c1ff")
frame.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

photo = tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
photo=photo.subsample(3,3)
button=tk.Button(frame,text="Click",bg="gray",image=photo,command='LEFT')
button.pack()
root.mainloop()