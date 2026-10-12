
import tkinter as tk #tkinter is built in library to create dekstop interface
import json 
from pathlib import Path
import os 
import shutil


APP_FOLDER = Path(os.environ["APPDATA"]) / "MyStickyNotes"
APP_FOLDER.mkdir(parents=True, exist_ok=True)

SAVE_FILE = APP_FOLDER / "my_sticky_notes.json"

OLD_SAVE_FILE = Path(__file__).parent / "my_sticky_notes.json"

if not SAVE_FILE.exists() and OLD_SAVE_FILE.exists():
    shutil.copy2(OLD_SAVE_FILE, SAVE_FILE)

notes = [] # creates empty python list
loading = False


# this creates our main application window
root = tk.Tk() #tk gives it a shorter name, here root is a variable, tk.Tk creates our main application window

root.title("My Sticky Notes")          # window's title bar
root.geometry("400x400")               # size of window, NOT STICKY NOTE
root.withdraw() #hides main window but keeps apps running 



def create_note(saved_title="", saved_content=""):                     # created a function, when runs shows new note clicked in terminal
    note = tk.Toplevel(root)           # create another window belonging to same application, can create many
    note.overrideredirect(True)
    note.geometry("250x250")
    note.configure(bg="#FFF2A8")

    # Custom yellow title bar
    header = tk.Frame(note, bg="#F2D46B", height=30)
    header.pack(fill="x")
    header.pack_propagate(False)

    

    # Darker yellow close button
    close_button = tk.Button(
        header,
        text="✕",
        bg="#D9B94E",
        fg="#5C4700",
        bd=0,
        activebackground="#C9A63D",
        command=note.destroy
    )
    close_button.pack(side="right", fill="y")
    def send_to_back():
        note.attributes("-topmost", False)
        note.lower()

    # Pin button
    pin_button = tk.Button(
        header,
        text="📌",
        bg="#D9B94E",
        fg="#5C4700",
        bd=0,
        activebackground="#C9A63D",
        command=send_to_back
    )
    pin_button.pack(side="right", fill="y")



    # Move the sticky note by dragging its header
    def start_move(event):
        note.start_x = event.x_root - note.winfo_x()
        note.start_y = event.y_root - note.winfo_y()

    def move_note(event):
        x = event.x_root - note.start_x
        y = event.y_root - note.start_y
        note.geometry(f"+{x}+{y}")

    header.bind("<Button-1>", start_move)
    header.bind("<B1-Motion>", move_note)

    # allow to edit text in the sticky note 
    title = tk.Entry(  # Entry is single line text input, to allow them to put/edit title
        note,          # means input belongs inside sticky note
        font=("Arial",14,"bold"),
        bg="#FFF2A8",
        bd=0  #removes border
    )
    title.pack(fill="x", padx=10, pady=10)
    title.insert(0, saved_title)

    # create a larger text area

    #for ur notes inside 
    content = tk.Text(
        note,      #same, its for putting text in sticky note
        font=("Arial", 11),
        bg="#FFF2A8",
        bd=0,
        wrap="word" # means long sentence auto continue on next line and not cut off horizontally
    )
    content.pack(   #arranging widgets
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    content.insert("1.0", saved_content)

    notes.append({
        "title":title,
        "content":content
    })

    title.bind("<KeyRelease>", auto_save)
    content.bind("<KeyRelease>", auto_save)

    if not loading:
        save_notes()


def save_notes():
    saved_data =[]
    print("Number of notes:", len(notes))
    print("Saving to:", SAVE_FILE)

    for note in notes:  # loop through every note
        if not note["title"].winfo_exists():
            continue

        note_info = {  #create a dictionary
            "title":note["title"].get(),
            "content": note["content"].get("1.0", "end-1c")

        }
        saved_data.append(note_info)  #add dictionary to our lsit 
        print("Note data:", note_info)

    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(saved_data, file, indent=4)

    print("Notes saved successfully!")
    print("File size:", SAVE_FILE.stat().st_size, "bytes")


def auto_save(event=None):
    if not loading:
        save_notes()
    

def load_notes():
    global loading

    if not SAVE_FILE.exists():   #check whether file exists 
        return

    with open(SAVE_FILE, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    loading = True

    try:
        for note in saved_data:
            create_note(
                note["title"],
                note["content"]
            )
    finally:
        loading = False


new_button = tk.Button( # tk.Button creates a button
    root,               # tells tkinter which window the button belongs to
    text ="+ New Note", # determines the buttons label
    command=lambda: create_note() # tell python to execute when button is clicked
)

new_button.pack(pady=20)

save_button = tk.Button(
    root,
    text="Save Notes",
    command=save_notes
)

save_button.pack(pady=10)


def close_app():
    save_notes()
    root.withdraw()


root.protocol("WM_DELETE_WINDOW", close_app)

def open_settings(event=None):
    root.deiconify()
    root.lift()
    root.focus_force()

root.bind_all("<Control-p>", open_settings)

load_notes()
root.mainloop() # mainloop keeps the application running, listening for events, mouse clicks, keyboard and window closing
