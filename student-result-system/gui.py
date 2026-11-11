
import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()

# Window settings
root.title("Student Result Management System")
root.geometry("900x600")
root.resizable(True, True)

# Main heading
title_label = tk.Label(
    root,
    text="STUDENT RESULT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#1f4e79",
    pady=20
)
title_label.pack(fill="x")

# Welcome message
welcome_label = tk.Label(
    root,
    text="Welcome! Manage student records and academic results.",
    font=("Arial", 12),
    pady=20
)
welcome_label.pack()

# Main content frame
main_frame = tk.Frame(root, padx=30, pady=20)
main_frame.pack(fill="both", expand=True)

# Section heading
section_label = tk.Label(
    main_frame,
    text="Dashboard",
    font=("Arial", 16, "bold")
)
section_label.pack(pady=10)

# Buttons
register_button = ttk.Button(
    main_frame,
    text="Register Student"
)
register_button.pack(pady=8, ipadx=20)

scores_button = ttk.Button(
    main_frame,
    text="Enter Student Scores"
)
scores_button.pack(pady=8, ipadx=20)

view_button = ttk.Button(
    main_frame,
    text="View Student Results"
)
view_button.pack(pady=8, ipadx=20)

search_button = ttk.Button(
    main_frame,
    text="Search Student"
)
search_button.pack(pady=8, ipadx=20)

best_button = ttk.Button(
    main_frame,
    text="Best Performing Student"
)
best_button.pack(pady=8, ipadx=20)

lowest_button = ttk.Button(
    main_frame,
    text="Lowest Performing Student"
)
lowest_button.pack(pady=8, ipadx=20)

# Exit button
exit_button = ttk.Button(
    main_frame,
    text="Exit",
    command=root.destroy
)
exit_button.pack(pady=20, ipadx=30)

# Start the application
root.mainloop()
