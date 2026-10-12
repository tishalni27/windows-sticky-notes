
import tkinter as tk #tkinter is built in library to create dekstop interface
import json
from pathlib import Path
import os
import shutil
from settings import setup_settings

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


def open_settings(event=None):
    # Show the main control window
    root.deiconify()
    root.lift()
    root.focus_force()


def create_note(saved_title="", saved_content="", color="#FFF2A8"):
    # created a function, when runs shows new note clicked in terminal
    note = tk.Toplevel(root)           # create another window belonging to same application, can create many
    note.overrideredirect(True)
    note.geometry("250x250")
    note.configure(bg=color)

    # Custom yellow title bar
    # Custom title bar matching the sticky note color
    HEADER_COLORS = {
        "#FFF2A8": "#F2D46B",  # Yellow
        "#FFD6E7": "#F2A8C6",  # Pink
        "#CDE9FF": "#91C9F2",  # Blue
        "#D8F5D0": "#A5D99A"   # Green
    }

    header_color = HEADER_COLORS.get(color, "#F2D46B")

    header = tk.Frame(note, bg=header_color, height=30)
    header.pack(fill="x")
    header.pack_propagate(False)

    # Darker yellow close button
    def close_note():
        # Remove this note from the screen and save remaining notes
        note.destroy()
        save_notes()

    close_button = tk.Button(
        header,
        text="✕",
        bg=header_color,
        fg="#5C4700",
        bd=0,
        activebackground=header_color,
        command=close_note
    )
    close_button.pack(side="right", fill="y")

    def send_to_back():
        note.attributes("-topmost", False)
        note.lower()

    # Pin button
    pin_button = tk.Button(
        header,
        text="📌",
        bg=header_color,
        fg="#5C4700",
        bd=0,
        activebackground=header_color,
        command=send_to_back
    )
    pin_button.pack(side="right", fill="y")

    # Plus button to open the settings window
    plus_button = tk.Button(
        header,
        text="+",
        bg=header_color,
        fg="#5C4700",
        bd=0,
        font=("Arial", 14, "bold"),
        activebackground=header_color,
        command=open_settings
    )
    plus_button.pack(side="right", fill="y")

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
        bg=color,
        bd=0  #removes border
    )
    title.pack(fill="x", padx=10, pady=10)
    title.insert(0, saved_title)

    # create a larger text area

    #for ur notes inside
    content = tk.Text(
        note,      #same, its for putting text in sticky note
        font=("Arial", 11),
        bg=color,
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
        "window": note,
        "title": title,
        "content": content,
        "color": color
    })

    title.bind("<KeyRelease>", auto_save)
    content.bind("<KeyRelease>", auto_save)

    if not loading:
        save_notes()


def save_notes():
    saved_data = []
    print("Number of notes:", len(notes))
    print("Saving to:", SAVE_FILE)

    for note in notes:  # loop through every note
        if not note["title"].winfo_exists():
            continue

        note_info = {  #create a dictionary
            "title": note["title"].get(),
            "content": note["content"].get("1.0", "end-1c"),
            "color": note["color"]
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

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            saved_data = json.load(file)
    except json.JSONDecodeError:
        print("JSON file is empty or invalid. No notes loaded.")
        return

    loading = True

    try:
        for note in saved_data:
            create_note(
                note.get("title", ""),
                note.get("content", ""),
                note.get("color", "#FFF2A8")
            )
    finally:
        loading = False


# Load the settings interface from settings.py
setup_settings(root, create_note)


def close_app():
    save_notes()
    root.withdraw()


root.protocol("WM_DELETE_WINDOW", close_app)

root.bind_all("<Control-p>", open_settings)

load_notes()

# If there are no saved notes, open settings automatically
if not any(note["window"].winfo_exists() for note in notes):
    open_settings()

root.mainloop() # mainloop keeps the application running, listening for events, mouse clicks, keyboard and window closing
