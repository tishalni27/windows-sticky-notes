import tkinter as tk #tkinter is built in library to create dekstop interface


# this creates our main application window
root = tk.Tk() #tk gives it a shorter name, here root is a variable, tk.Tk creates our main application window

root.title("My Sticky Notes") #window's title bar
root.geometry("400x300") #size of window
root.mainloop() # mainloop keeps the application running, listening for events, mouse clicks, keyboard and window closing
