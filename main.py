import tkinter as tk #tkinter is built in library to create dekstop interface


# this creates our main application window
root = tk.Tk() #tk gives it a shorter name, here root is a variable, tk.Tk creates our main application window

root.title("My Sticky Notes")          #window's title bar
root.geometry("400x400")               #size of window



def create_note():                     # created a function, when runs shows new note clicked in terminal
    print("New note clicked!")


new_button = tk.Button( # tk.Button creates a button
    root,               # tells tkinter which window the button belongs to
    text ="+ New Note", # determines the buttons label
    command = create_note # tell python to execute when button is clicked
)

new_button.pack(pady=20)

root.mainloop() # mainloop keeps the application running, listening for events, mouse clicks, keyboard and window closing


