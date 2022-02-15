#  	# Harry Houdini
# # CS 100 2021F Section 199
# # HW 03, September 17, 2021

# import turtle

# t=turtle.Turtle()
# # s=turtle.Screen()
# #equilateral triangle, 
# t.pendown()
# t.fd(100)
# t.rt(120)
# t.fd(100)
# t.rt(120)
# t.fd(100)
# t.rt(120)

# # a square
# t.fd(100)
# t.rt(90)
# t.fd(100)
# t.rt(90)
# t.fd(100)
# t.rt(90)
# t.fd(100)
# t.rt(90)
# # a regular pentagon, each with side length 100
# t.fd(100)
# t.rt(72)
# t.fd(100)
# t.rt(72)
# t.fd(100)
# t.rt(72)
# t.fd(100)
# t.rt(72)
# t.fd(100)
# t.rt(72)

def factorial(n):
    if n==1:
        return 1
    return n*factorial(n-1)

def logR(n):
    if n==2:
        return 1
    ans=logR(n/2)
    return
print(factorial(100))