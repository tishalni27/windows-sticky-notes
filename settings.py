
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
    root.title("My Sticky Notes | Settings")
    root.geometry("390x430")
    root.resizable(False, False)
    root.configure(bg="#F7F8FA")

    # Main content container
    container = tk.Frame(
        root,
        bg="#F7F8FA"
    )
    container.pack(
        fill="both",
        expand=True,
        padx=28,
        pady=25
    )

    # Heading
    heading = tk.Label(
        container,
        text="My Sticky Notes",
        font=("Segoe UI", 22, "bold"),
        fg="#252A32",
        bg="#F7F8FA"
    )
    heading.pack(anchor="w")

    # Subtitle
    subtitle = tk.Label(
        container,
        text="Capture ideas, reminders and little thoughts.",
        font=("Segoe UI", 10),
        fg="#747B86",
        bg="#F7F8FA"
    )
    subtitle.pack(anchor="w", pady=(5, 25))

    # Button to create a new note
    new_button = tk.Button(
        container,
        text="+  Create New Note",
        font=("Segoe UI", 12, "bold"),
        bg="#30343B",
        fg="white",
        activebackground="#454B55",
        activeforeground="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        height=2,
        command=lambda: create_note()
    )
    new_button.pack(fill="x")

    # Color selection heading
    color_label = tk.Label(
        container,
        text="CHOOSE A COLOR",
        font=("Segoe UI", 9, "bold"),
        fg="#747B86",
        bg="#F7F8FA"
    )
    color_label.pack(anchor="w", pady=(30, 12))

    # Container for color buttons
    colors_frame = tk.Frame(
        container,
        bg="#F7F8FA"
    )
    colors_frame.pack(fill="x")

    # Create a button for every color
    for index, (color_name, color_code) in enumerate(COLORS.items()):

        color_button = tk.Button(
            colors_frame,
            text=color_name,
            font=("Segoe UI", 11),
            bg=color_code,
            fg="#30343B",
            activebackground=color_code,
            bd=0,
            relief="flat",
            cursor="hand2",
            height=2,
            command=lambda c=color_code: create_note(color=c)
        )

        color_button.grid(
            row=index // 2,
            column=index % 2,
            padx=5,
            pady=5,
            sticky="ew"
        )

    colors_frame.columnconfigure(0, weight=1)
    colors_frame.columnconfigure(1, weight=1)

    # Footer
    footer = tk.Label(
        container,
        text="Your notes are saved automatically.",
        font=("Segoe UI", 9),
        fg="#9298A1",
        bg="#F7F8FA"
    )
    footer.pack(side="bottom", pady=(20, 0))
