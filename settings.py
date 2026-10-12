
import tkinter as tk

# Available sticky note colors
COLORS = {
    "Yellow": "#FFF2A8",
    "Pink": "#FFD6E7",
    "Blue": "#CDE9FF",
    "Green": "#D8F5D0"
}


def setup_settings(root, create_note):

    # Create the settings window design
    root.title("Sticky Notes Settings")
    root.geometry("350x350")
    root.configure(bg="#FFFDF5")

    # Heading
    heading = tk.Label(
        root,
        text="My Sticky Notes",
        font=("Arial", 18, "bold"),
        bg="#FFFDF5"
    )
    heading.pack(pady=20)

    # Button to create a new note
    new_button = tk.Button(
        root,
        text="+ New Note",
        font=("Arial", 12),
        command=create_note
    )
    new_button.pack(pady=10)

    # Color selection heading
    color_label = tk.Label(
        root,
        text="Choose Note Color",
        font=("Arial", 12, "bold"),
        bg="#FFFDF5"
    )
    color_label.pack(pady=10)

    # Create a button for every color
    for color_name, color_code in COLORS.items():

        color_button = tk.Button(
            root,
            text=color_name,
            bg=color_code,
            width=20,
            command=lambda c=color_code: create_note(color=c)
        )
        color_button.pack(pady=4)
