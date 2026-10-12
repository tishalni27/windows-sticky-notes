
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

# Matching colors for each sticky note
NOTE_THEMES = {
    "#FFF2A8": {"header": "#F2D46B", "hover": "#E5C453"},
    "#FFD6E7": {"header": "#F2A8C6", "hover": "#E68EB3"},
    "#CDE9FF": {"header": "#91C9F2", "hover": "#74B6E8"},
    "#D8F5D0": {"header": "#A5D99A", "hover": "#89C77D"}
}

TEXT_COLOR = "#30343B"

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


def create_note(saved_title="", saved_content="", color="#FFF2A8",
                x=None, y=None, width=300, height=320):
    # created a function, when runs shows new note clicked in terminal

    theme = NOTE_THEMES.get(color, NOTE_THEMES["#FFF2A8"])
    header_color = theme["header"]
    hover_color = theme["hover"]

    note = tk.Toplevel(root)           # create another window belonging to same application, can create many
    note.overrideredirect(True)

    # New notes are slightly larger for easier writing
    if x is None or y is None:
        offset = (len(notes) % 6) * 28
        x = 120 + offset
        y = 120 + offset

    width = max(200, int(width))
    height = max(180, int(height))

    note.geometry(f"{width}x{height}+{x}+{y}")
    note.configure(bg=color)

    # Custom yellow title bar
    # Custom title bar matching the sticky note color
    header = tk.Frame(note, bg=header_color, height=38)
    header.pack(fill="x")
    header.pack_propagate(False)

    # Small application label
    header_label = tk.Label(
        header,
        text="NOTE",
        font=("Segoe UI", 9, "bold"),
        bg=header_color,
        fg=TEXT_COLOR
    )
    header_label.pack(side="left", padx=14)

    # Darker yellow close button
    def close_note():
        # Remove this note from the screen and save remaining notes
        note.destroy()
        notes[:] = [
            n for n in notes if n["window"] != note
        ]
        save_notes()

        # If all notes are closed, show settings
        if not notes:
            open_settings()

    def send_to_back():
        note.attributes("-topmost", False)
        note.lower()

    # Reusable button design
    def make_header_button(symbol, command):
        button = tk.Button(
            header,
            text=symbol,
            font=("Segoe UI", 12),
            bg=header_color,
            fg=TEXT_COLOR,
            bd=0,
            relief="flat",
            width=3,
            cursor="hand2",
            activebackground=hover_color,
            activeforeground=TEXT_COLOR,
            highlightthickness=0,
            command=command
        )

        button.pack(side="right", fill="y")

        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover_color)
        )
        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=header_color)
        )

        return button

    # Close button
    close_button = make_header_button("✕", close_note)

    # Pin button
    pin_button = make_header_button("📌", send_to_back)

    # Plus button to open the settings window
    plus_button = make_header_button("+", open_settings)

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
    header_label.bind("<Button-1>", start_move)
    header_label.bind("<B1-Motion>", move_note)

    # Save the note's new position after dragging
    header.bind("<ButtonRelease-1>", lambda event: save_notes())
    header_label.bind("<ButtonRelease-1>", lambda event: save_notes())

    # allow to edit text in the sticky note
    title = tk.Entry(  # Entry is single line text input, to allow them to put/edit title
        note,          # means input belongs inside sticky note
        font=("Segoe UI", 15, "bold"),
        bg=color,
        fg=TEXT_COLOR,
        bd=0,  #removes border
        insertbackground=TEXT_COLOR,
        highlightthickness=0
    )
    title.pack(fill="x", padx=16, pady=(18, 12))
    title.insert(0, saved_title)

    # Underline divider separating title and content
    title_line = tk.Frame(
        note,
        bg=header_color,
        height=1
    )
    title_line.pack(fill="x", padx=16, pady=(0, 8))

    # create a larger text area

    #for ur notes inside
    content = tk.Text(
        note,      #same, its for putting text in sticky note
        font=("Segoe UI", 11),
        bg=color,
        fg=TEXT_COLOR,
        bd=0,
        wrap="word", # means long sentence auto continue on next line and not cut off horizontally
        insertbackground=TEXT_COLOR,
        highlightthickness=0,
        undo=True,
        padx=2,
        pady=4
    )

    content.pack(   #arranging widgets
        fill="both",
        expand=True,
        padx=14,
        pady=(0, 14)
    )

    content.insert("1.0", saved_content)

    # Press Enter in the title to move cursor into content
    def move_to_content(event):
        content.focus_set()
        content.mark_set("insert", "1.0")
        return "break"

    title.bind("<Return>", move_to_content)

    # Resize the sticky note by dragging the bottom-right handle
    resize_state = {}

    def start_resize(event):
        resize_state["start_x"] = event.x_root
        resize_state["start_y"] = event.y_root
        resize_state["width"] = note.winfo_width()
        resize_state["height"] = note.winfo_height()

    def resize_note(event):
        if "start_x" not in resize_state:
            return

        dx = event.x_root - resize_state["start_x"]
        dy = event.y_root - resize_state["start_y"]

        new_width = max(200, resize_state["width"] + dx)
        new_height = max(180, resize_state["height"] + dy)

        note.geometry(f"{new_width}x{new_height}")

    def stop_resize(event):
        resize_state.clear()
        save_notes()

    # Visible resize handle
    resize_handle = tk.Label(
        note,
        text="◢",
        font=("Segoe UI", 12),
        bg=color,
        fg=header_color,
        cursor="size_nw_se"
    )

    resize_handle.place(
        relx=1.0,
        rely=1.0,
        anchor="se"
    )

    resize_handle.bind("<ButtonPress-1>", start_resize)
    resize_handle.bind("<B1-Motion>", resize_note)
    resize_handle.bind("<ButtonRelease-1>", stop_resize)

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

    # Bring newly created note forward
    note.lift()
    return note


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
            "color": note["color"],
            "x": note["window"].winfo_x(),
            "y": note["window"].winfo_y(),
            "width": note["window"].winfo_width(),
            "height": note["window"].winfo_height()
        }

        saved_data.append(note_info)  #add dictionary to our lsit
        print("Note data:", note_info)

    # Write safely using a temporary file
    temporary_file = SAVE_FILE.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(saved_data, file, indent=4)

    os.replace(temporary_file, SAVE_FILE)

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
    except (json.JSONDecodeError, OSError):
        print("JSON file is empty or invalid. No notes loaded.")
        return

    if not isinstance(saved_data, list):
        return

    loading = True

    try:
        for note in saved_data:
            create_note(
                note.get("title", ""),
                note.get("content", ""),
                note.get("color", "#FFF2A8"),
                note.get("x"),
                note.get("y"),
                note.get("width", 300),
                note.get("height", 320)
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

# Open notes first, unless no saved notes exist
if not notes:
    open_settings()
else:
    root.withdraw()

root.mainloop() # mainloop keeps the application running, listening for events, mouse clicks, keyboard and window closing
