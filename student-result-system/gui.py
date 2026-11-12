import tkinter as tk
from tkinter import ttk, messagebox
import authentication
import main


# Load the existing student records from students.json
main.load_students()


# -------------------- COLOURS --------------------

NAVY = "#14213D"
NAVY_LIGHT = "#1E3157"
BLUE = "#3B82F6"
BLUE_LIGHT = "#EAF2FF"
PURPLE = "#8B5CF6"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
RED = "#EF4444"
BG = "#F4F7FB"
WHITE = "#FFFFFF"
DARK = "#172033"
MUTED = "#718096"
BORDER = "#E5EAF2"


# -------------------- MAIN WINDOW --------------------

root = tk.Tk()
root.title("EduStack | Student Result Management")
root.geometry("1240x780")
root.minsize(1050, 680)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background=WHITE,
    foreground=DARK,
    fieldbackground=WHITE,
    rowheight=38,
    borderwidth=0,
    font=("Segoe UI", 10),
)
style.configure(
    "Treeview.Heading",
    background="#F0F4FA",
    foreground=MUTED,
    relief="flat",
    font=("Segoe UI", 9, "bold"),
    padding=(10, 12),
)
style.map(
    "Treeview",
    background=[("selected", BLUE_LIGHT)],
    foreground=[("selected", NAVY)],
)
style.configure("Vertical.TScrollbar", background="#DCE4EF", troughcolor=WHITE)


# -------------------- APP LAYOUT --------------------

sidebar = tk.Frame(root, bg=NAVY, width=238)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main_area = tk.Frame(root, bg=BG)
main_area.pack(side="right", fill="both", expand=True)

topbar = tk.Frame(main_area, bg=WHITE, height=72)
topbar.pack(side="top", fill="x")
topbar.pack_propagate(False)

page_area = tk.Frame(main_area, bg=BG)
page_area.pack(fill="both", expand=True)


# -------------------- SHARED HELPERS --------------------

def clear_page():
    for widget in page_area.winfo_children():
        widget.destroy()


def validate_student_name(name):
    """Simple local validation; does not depend on main.py."""
    cleaned = name.strip()
    return bool(cleaned) and any(character.isalpha() for character in cleaned)


def find_student(registration):
    registration = registration.strip().lower()
    for student in main.students:
        if student.get("reg_no", "").lower() == registration:
            return student
    return None


def get_scored_students():
    return [
        student for student in main.students
        if student.get("average") is not None
    ]


def make_button(parent, text, command, primary=True, width=None):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        font=("Segoe UI", 10, "bold"),
        bg=BLUE if primary else WHITE,
        fg=WHITE if primary else DARK,
        activebackground="#2563EB" if primary else BLUE_LIGHT,
        activeforeground=WHITE if primary else NAVY,
        relief="flat",
        bd=0,
        padx=18,
        pady=11,
        cursor="hand2",
    )


def make_card(parent, title, value, accent, note):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        padx=18,
        pady=17,
    )
    tk.Frame(card, bg=accent, height=4).pack(fill="x", side="top")
    tk.Label(
        card, text=title.upper(), bg=WHITE, fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", pady=(13, 7))
    tk.Label(
        card, text=str(value), bg=WHITE, fg=DARK,
        font=("Segoe UI", 25, "bold")
    ).pack(anchor="w")
    tk.Label(
        card, text=note, bg=WHITE, fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(anchor="w", pady=(5, 0))
    return card


def page_heading(title, subtitle):
    heading = tk.Frame(page_area, bg=BG)
    heading.pack(fill="x", padx=30, pady=(25, 20))
    tk.Label(
        heading, text=title, bg=BG, fg=DARK,
        font=("Segoe UI", 23, "bold")
    ).pack(anchor="w")
    tk.Label(
        heading, text=subtitle, bg=BG, fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(5, 0))


def section_title(parent, title, subtitle=None):
    tk.Label(
        parent, text=title, bg=WHITE, fg=DARK,
        font=("Segoe UI", 14, "bold")
    ).pack(anchor="w")
    if subtitle:
        tk.Label(
            parent, text=subtitle, bg=WHITE, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(4, 12))


def add_labeled_entry(parent, label, placeholder=None):
    wrapper = tk.Frame(parent, bg=WHITE)
    wrapper.pack(fill="x", pady=8)
    tk.Label(
        wrapper, text=label, bg=WHITE, fg=DARK,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(0, 6))
    entry = ttk.Entry(wrapper, font=("Segoe UI", 11))
    entry.pack(fill="x", ipady=7)
    return entry


def show_result_window(student):
    window = tk.Toplevel(root)
    window.title("Student Result")
    window.geometry("480x570")
    window.configure(bg=BG)
    window.transient(root)

    banner = tk.Frame(window, bg=NAVY, padx=25, pady=22)
    banner.pack(fill="x")
    tk.Label(
        banner, text="STUDENT RESULT", bg=NAVY, fg=WHITE,
        font=("Segoe UI", 17, "bold")
    ).pack(anchor="w")
    tk.Label(
        banner, text=student.get("name", ""), bg=NAVY, fg="#C7D7F2",
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(5, 0))

    body = tk.Frame(window, bg=WHITE, padx=25, pady=22)
    body.pack(fill="both", expand=True, padx=18, pady=18)

    tk.Label(
        body, text=f"Registration number: {student.get('reg_no', '')}",
        bg=WHITE, fg=MUTED, font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 15))

    if student.get("average") is None:
        tk.Label(
            body, text="Scores have not been entered yet.",
            bg=WHITE, fg=ORANGE, font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=15)
        return

    for subject in main.SUBJECTS:
        score = student.get("subjects", {}).get(subject, "-")
        row = tk.Frame(body, bg="#F7F9FC", padx=12, pady=10)
        row.pack(fill="x", pady=4)
        tk.Label(
            row, text=subject, bg="#F7F9FC", fg=DARK,
            font=("Segoe UI", 10)
        ).pack(side="left")
        tk.Label(
            row, text=str(score), bg="#F7F9FC", fg=NAVY,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right")

    tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=14)
    tk.Label(
        body, text=f"Total score: {student.get('total', 0):g}",
        bg=WHITE, fg=DARK, font=("Segoe UI", 11)
    ).pack(anchor="w", pady=4)
    tk.Label(
        body, text=f"Average: {student['average']:.2f}%",
        bg=WHITE, fg=BLUE, font=("Segoe UI", 15, "bold")
    ).pack(anchor="w", pady=6)
    tk.Label(
        body, text=f"Grade: {student.get('grade', '-')}",
        bg=WHITE, fg=GREEN, font=("Segoe UI", 22, "bold")
    ).pack(anchor="w", pady=5)


def refresh_dashboard():
    show_dashboard()


# -------------------- DASHBOARD --------------------

def show_dashboard():
    set_active_nav("Dashboard")
    clear_page()
    page_heading("Dashboard", "Here's an overview of your student records and academic results.")

    scored = get_scored_students()
    total = len(main.students)
    highest = max((s["average"] for s in scored), default=0)
    lowest = min((s["average"] for s in scored), default=0)

    cards = tk.Frame(page_area, bg=BG)
    cards.pack(fill="x", padx=24)
    card_data = [
        ("Total students", total, BLUE, "Registered students"),
        ("Results entered", len(scored), GREEN, "Students with scores"),
        ("Highest average", f"{highest:.2f}%", PURPLE, "Top class average"),
        ("Lowest average", f"{lowest:.2f}%", ORANGE, "Lowest class average"),
    ]
    for title, value, colour, note in card_data:
        card = make_card(cards, title, value, colour, note)
        card.pack(side="left", fill="both", expand=True, padx=6)

    lower = tk.Frame(page_area, bg=BG)
    lower.pack(fill="both", expand=True, padx=30, pady=22)

    recent_panel = tk.Frame(
        lower, bg=WHITE, padx=18, pady=18,
        highlightbackground=BORDER, highlightthickness=1
    )
    recent_panel.pack(side="left", fill="both", expand=True, padx=(0, 12))
    section_title(recent_panel, "Recently registered students",
                  "A quick view of the latest student records")

    columns = ("name", "registration", "average", "grade")
    table = ttk.Treeview(recent_panel, columns=columns, show="headings", height=9)
    for col, label, width in [
        ("name", "STUDENT NAME", 220),
        ("registration", "REGISTRATION NUMBER", 150),
        ("average", "AVERAGE", 100),
        ("grade", "GRADE", 70),
    ]:
        table.heading(col, text=label)
        table.column(col, width=width, anchor="w" if col == "name" else "center")
    for student in reversed(main.students[-10:]):
        average = student.get("average")
        table.insert(
            "", "end",
            values=(
                student.get("name", ""),
                student.get("reg_no", ""),
                f"{average:.2f}%" if average is not None else "Pending",
                student.get("grade") or "-",
            ),
        )
    table.pack(fill="both", expand=True)

    quick_panel = tk.Frame(
        lower, bg=WHITE, width=230, padx=18, pady=18,
        highlightbackground=BORDER, highlightthickness=1
    )
    quick_panel.pack(side="right", fill="y")
    quick_panel.pack_propagate(False)
    section_title(quick_panel, "Quick actions", "Common tasks")
    for label, command in [
        ("＋  Register student", show_register_page),
        ("✎  Enter scores", show_scores_page),
        ("▤  View all results", show_results_page),
        ("⌕  Search student", show_search_page),
    ]:
        tk.Button(
            quick_panel, text=label, command=command,
            anchor="w", bg="#F5F8FE", fg=NAVY,
            activebackground=BLUE_LIGHT, relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), padx=12, pady=13,
            cursor="hand2"
        ).pack(fill="x", pady=6)


# -------------------- REGISTER STUDENT --------------------

def show_register_page():
    set_active_nav("Register Student")
    clear_page()
    page_heading("Register student", "Add a new student to the system.")

    panel = tk.Frame(
        page_area, bg=WHITE, padx=28, pady=25,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(anchor="nw", fill="x", padx=30, pady=5)

    section_title(panel, "Student information",
                  "Enter the student's name and unique registration number.")

    name_entry = add_labeled_entry(panel, "Full name")
    registration_entry = add_labeled_entry(panel, "Registration number")

    def save_student():
        name = name_entry.get().strip()
        registration = registration_entry.get().strip()

        if not name or not registration:
            messagebox.showerror("Missing information", "Please fill in both fields.", parent=root)
            return
        if not validate_student_name(name):
            messagebox.showerror("Invalid name", "Please enter a valid student name.", parent=root)
            return
        if find_student(registration):
            messagebox.showerror("Duplicate record", "That registration number already exists.", parent=root)
            return

        main.students.append({
            "name": name,
            "reg_no": registration,
            "subjects": {},
            "total": None,
            "average": None,
            "grade": None,
        })
        main.save_students()
        messagebox.showinfo("Success", "Student registered successfully.", parent=root)
        show_dashboard()

    actions = tk.Frame(panel, bg=WHITE)
    actions.pack(fill="x", pady=(20, 0))
    make_button(actions, "Save student", save_student).pack(side="left")
    make_button(actions, "Cancel", show_dashboard, primary=False).pack(side="left", padx=10)


# -------------------- ENTER SCORES --------------------

def show_scores_page():
    set_active_nav("Enter Scores")
    clear_page()
    page_heading("Enter student scores", "Record subject scores and calculate the student's result.")

    panel = tk.Frame(
        page_area, bg=WHITE, padx=28, pady=25,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(anchor="nw", fill="x", padx=30, pady=5)
    section_title(panel, "Score information", "Scores must be numbers between 0 and 100.")

    registration_entry = add_labeled_entry(panel, "Registration number")
    score_entries = {}
    for subject in main.SUBJECTS:
        score_entries[subject] = add_labeled_entry(panel, f"{subject} score")

    def save_scores():
        student = find_student(registration_entry.get())
        if not registration_entry.get().strip():
            messagebox.showerror("Missing information", "Enter a registration number.", parent=root)
            return
        if student is None:
            messagebox.showerror("Student not found", "No student has that registration number.", parent=root)
            return

        scores = {}
        for subject, entry in score_entries.items():
            try:
                score = float(entry.get())
            except ValueError:
                messagebox.showerror("Invalid score", f"Enter a number for {subject}.", parent=root)
                return
            if not 0 <= score <= 100:
                messagebox.showerror("Invalid score", f"{subject} must be between 0 and 100.", parent=root)
                return
            scores[subject] = score

        total = sum(scores.values())
        average = total / len(main.SUBJECTS)
        student["subjects"] = scores
        student["total"] = total
        student["average"] = average
        student["grade"] = main.calculate_grade(average)
        main.save_students()
        messagebox.showinfo("Success", "Student scores saved successfully.", parent=root)
        show_dashboard()

    actions = tk.Frame(panel, bg=WHITE)
    actions.pack(fill="x", pady=(20, 0))
    make_button(actions, "Save scores", save_scores).pack(side="left")
    make_button(actions, "Cancel", show_dashboard, primary=False).pack(side="left", padx=10)


# -------------------- ALL RESULTS --------------------

def show_results_page():
    set_active_nav("View All Results")
    clear_page()
    page_heading("Student results", "Browse scores, totals, averages and grades for all students.")

    panel = tk.Frame(
        page_area, bg=WHITE, padx=18, pady=18,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(fill="both", expand=True, padx=30, pady=5)

    columns = ("name", "registration", "maths", "english", "biology", "total", "average", "grade")
    table = ttk.Treeview(panel, columns=columns, show="headings")
    headings = {
        "name": "STUDENT", "registration": "REGISTRATION NO.",
        "maths": "MATHEMATICS", "english": "ENGLISH",
        "biology": "BIOLOGY", "total": "TOTAL",
        "average": "AVERAGE", "grade": "GRADE",
    }
    for col in columns:
        table.heading(col, text=headings[col])
        table.column(col, width=115, anchor="center")
    table.column("name", width=160, anchor="w")
    table.column("registration", width=130)

    for student in main.students:
        subjects = student.get("subjects", {})
        average = student.get("average")
        if average is None:
            values = (
                student.get("name", ""), student.get("reg_no", ""),
                "-", "-", "-", "-", "Pending", "-",
            )
        else:
            values = (
                student.get("name", ""), student.get("reg_no", ""),
                subjects.get("Mathematics", "-"),
                subjects.get("English", "-"),
                subjects.get("Biology", "-"),
                student.get("total", "-"), f"{average:.2f}%",
                student.get("grade", "-"),
            )
        table.insert("", "end", values=values)

    y_scroll = ttk.Scrollbar(panel, orient="vertical", command=table.yview)
    x_scroll = ttk.Scrollbar(panel, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    table.pack(side="top", fill="both", expand=True)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")


# -------------------- SEARCH STUDENT --------------------

def show_search_page():
    set_active_nav("Search Student")
    clear_page()
    page_heading("Search student", "Find a student using their registration number.")

    panel = tk.Frame(
        page_area, bg=WHITE, padx=28, pady=25,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(anchor="nw", fill="x", padx=30, pady=5)
    section_title(panel, "Student lookup", "Enter the registration number to view the student's result.")

    registration_entry = add_labeled_entry(panel, "Registration number")

    def search():
        registration = registration_entry.get().strip()
        if not registration:
            messagebox.showerror("Missing information", "Enter a registration number.", parent=root)
            return
        student = find_student(registration)
        if student is None:
            messagebox.showerror("Not found", "No student matches that registration number.", parent=root)
            return
        show_result_window(student)

    actions = tk.Frame(panel, bg=WHITE)
    actions.pack(fill="x", pady=(20, 0))
    make_button(actions, "Search student", search).pack(side="left")


# -------------------- PERFORMERS --------------------

def show_performer(best=True):
    scored = get_scored_students()
    if not scored:
        messagebox.showinfo("No results", "There are no student results to compare yet.", parent=root)
        return

    student = (
        max(scored, key=lambda item: item["average"])
        if best else min(scored, key=lambda item: item["average"])
    )
    set_active_nav("Best Performer" if best else "Lowest Performer")
    clear_page()
    title = "Best performing student" if best else "Lowest performing student"
    page_heading(title, "Performance is based on the average score across all subjects.")

    panel = tk.Frame(
        page_area, bg=WHITE, padx=30, pady=28,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(anchor="nw", fill="x", padx=30, pady=5)

    accent = GREEN if best else ORANGE
    tk.Label(
        panel, text="TOP PERFORMANCE" if best else "PERFORMANCE SUMMARY",
        bg=WHITE, fg=accent, font=("Segoe UI", 10, "bold")
    ).pack(anchor="w")
    tk.Label(
        panel, text=student["name"], bg=WHITE, fg=DARK,
        font=("Segoe UI", 23, "bold")
    ).pack(anchor="w", pady=(10, 4))
    tk.Label(
        panel, text=f"Registration number: {student['reg_no']}",
        bg=WHITE, fg=MUTED, font=("Segoe UI", 10)
    ).pack(anchor="w")
    tk.Label(
        panel, text=f"{student['average']:.2f}%",
        bg=WHITE, fg=accent, font=("Segoe UI", 34, "bold")
    ).pack(anchor="w", pady=(20, 3))
    tk.Label(
        panel, text=f"Grade {student.get('grade', '-')}",
        bg=WHITE, fg=DARK, font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")
    make_button(panel, "View full result", lambda: show_result_window(student)).pack(anchor="w", pady=(22, 0))


# -------------------- SIDEBAR --------------------

nav_buttons = {}


def set_active_nav(active):
    for label, button in nav_buttons.items():
        if label == active:
            button.configure(bg=NAVY_LIGHT, fg=WHITE)
        else:
            button.configure(bg=NAVY, fg="#C7D2E5")


def add_nav_button(label, icon, command):
    button = tk.Button(
        sidebar,
        text=f"{icon}   {label}",
        command=command,
        anchor="w",
        bg=NAVY,
        fg="#C7D2E5",
        activebackground=NAVY_LIGHT,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        padx=22,
        pady=14,
        cursor="hand2",
    )
    button.pack(fill="x", padx=10, pady=3)
    nav_buttons[label] = button


# Brand area
brand = tk.Frame(sidebar, bg=NAVY, padx=22, pady=28)
brand.pack(fill="x")
tk.Label(
    brand, text="EduStack", bg=NAVY, fg=WHITE,
    font=("Segoe UI", 22, "bold")
).pack(anchor="w")
tk.Label(
    brand, text="STUDENT RESULT PORTAL", bg=NAVY, fg="#9FB4D8",
    font=("Segoe UI", 8, "bold")
).pack(anchor="w", pady=(4, 0))

tk.Label(
    sidebar, text="MAIN MENU", bg=NAVY, fg="#8196BA",
    font=("Segoe UI", 8, "bold")
).pack(anchor="w", padx=24, pady=(20, 10))

add_nav_button("Dashboard", "▦", show_dashboard)
add_nav_button("Register Student", "＋", show_register_page)
add_nav_button("Enter Scores", "✎", show_scores_page)
add_nav_button("View All Results", "▤", show_results_page)
add_nav_button("Search Student", "⌕", show_search_page)

tk.Label(
    sidebar, text="PERFORMANCE", bg=NAVY, fg="#8196BA",
    font=("Segoe UI", 8, "bold")
).pack(anchor="w", padx=24, pady=(24, 10))
add_nav_button("Best Performer", "★", lambda: show_performer(True))
add_nav_button("Lowest Performer", "☆", lambda: show_performer(False))

footer = tk.Frame(sidebar, bg=NAVY, padx=22, pady=20)
footer.pack(side="bottom", fill="x")
tk.Frame(footer, bg="#34476A", height=1).pack(fill="x", pady=(0, 14))
tk.Label(
    footer, text="EduStack Desktop", bg=NAVY, fg=WHITE,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w")
tk.Label(
    footer, text="Student Result Management  •  v2.1",
    bg=NAVY, fg="#9FB4D8", font=("Segoe UI", 8)
).pack(anchor="w", pady=(4, 0))


# -------------------- TOP BAR --------------------

top_left = tk.Frame(topbar, bg=WHITE)
top_left.pack(side="left", fill="y", padx=30)
tk.Label(
    top_left, text="Academic workspace", bg=WHITE, fg=DARK,
    font=("Segoe UI", 11, "bold")
).pack(anchor="w", pady=(15, 0))
tk.Label(
    top_left, text="Student records and performance overview",
    bg=WHITE, fg=MUTED, font=("Segoe UI", 8)
).pack(anchor="w", pady=(2, 0))

top_right = tk.Frame(topbar, bg=WHITE)
top_right.pack(side="right", padx=28)
tk.Label(
    top_right, text="ADMINISTRATOR", bg=WHITE, fg=NAVY,
    font=("Segoe UI", 9, "bold")
).pack(side="left", padx=(0, 10))
avatar = tk.Label(
    top_right, text="A", bg=BLUE_LIGHT, fg=BLUE,
    font=("Segoe UI", 11, "bold"), width=3, height=1
)
avatar.pack(side="right", pady=17)


# -------------------- AUTHENTICATION AND ROLE DASHBOARDS --------------------

current_user = None


def update_topbar_user(user):
    for widget in top_right.winfo_children():
        widget.destroy()

    role = user["role"].upper()

    tk.Label(
        top_right,
        text=role,
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 9, "bold")
    ).pack(side="left", padx=10)

    tk.Button(
        top_right,
        text="Logout",
        command=logout,
        bg=BLUE_LIGHT,
        fg=BLUE,
        relief="flat",
        font=("Segoe UI", 9, "bold"),
        padx=14,
        pady=8,
        cursor="hand2"
    ).pack(side="right")


def show_student_dashboard(user):
    clear_page()

    page_heading(
        "Student Dashboard",
        f"Welcome, {user['username']}! Here is your school overview."
    )

    tk.Label(
        page_area,
        text="STUDENT PORTAL",
        bg=BG,
        fg=BLUE,
        font=("Segoe UI", 11, "bold")
    ).pack(anchor="w", padx=30, pady=15)

    make_card(
        page_area,
        "Student ID",
        user["username"],
        BLUE,
        "Your registered account"
    )

    tk.Label(
        page_area,
        text="Quick Actions",
        bg=BG,
        fg=DARK,
        font=("Segoe UI", 15, "bold")
    ).pack(anchor="w", padx=30, pady=(25, 10))

    tk.Button(
        page_area,
        text="Mark Daily Attendance",
        command=lambda: messagebox.showinfo(
            "Attendance",
            "Daily attendance will be implemented in the next module."
        ),
        bg=BLUE,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=20,
        pady=12
    ).pack(anchor="w", padx=30, pady=8)

    tk.Button(
        page_area,
        text="View My Results",
        command=lambda: messagebox.showinfo(
            "Results",
            "Your personal results page will be connected soon."
        ),
        bg=GREEN,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=20,
        pady=12
    ).pack(anchor="w", padx=30, pady=8)


def show_teacher_dashboard(user):
    clear_page()

    page_heading(
        "Teacher Dashboard",
        f"Welcome, {user['username']}! Manage your academic activities."
    )

    tk.Label(
        page_area,
        text="TEACHER PORTAL",
        bg=BG,
        fg=GREEN,
        font=("Segoe UI", 11, "bold")
    ).pack(anchor="w", padx=30, pady=15)

    make_card(
        page_area,
        "Teacher ID",
        user["username"],
        GREEN,
        "Your registered account"
    )

    tk.Label(
        page_area,
        text="Teaching Activities",
        bg=BG,
        fg=DARK,
        font=("Segoe UI", 15, "bold")
    ).pack(anchor="w", padx=30, pady=(25, 10))

    actions = [
        "View Assigned Classes",
        "Monitor Student Attendance",
        "Enter Student Scores",
        "Compile Results"
    ]

    for action in actions:
        tk.Button(
            page_area,
            text=action,
            command=lambda name=action: messagebox.showinfo(
                name,
                f"{name} will be connected in the next development stage."
            ),
            bg=WHITE,
            fg=NAVY,
            relief="solid",
            bd=1,
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=12,
            cursor="hand2"
        ).pack(anchor="w", padx=30, pady=6)


def logout():
    global current_user

    current_user = None

    sidebar.pack_forget()
    main_area.pack_forget()

    show_login_page()


def handle_login(username_entry, password_entry):
    global current_user

    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please enter your username and password."
        )
        return

    user = authentication.login_user(username, password)

    if user is None:
        messagebox.showerror(
            "Login Failed",
            "Incorrect username or password."
        )
        return

    current_user = user

    # Remove the login screen
    login_frame.destroy()

    # Display the main application
    main_area.pack(side="right", fill="both", expand=True)
    update_topbar_user(user)

    if user["role"] == "admin":
        sidebar.pack(side="left", fill="y")
        show_dashboard()

    elif user["role"] == "teacher":
        sidebar.pack_forget()
        show_teacher_dashboard(user)

    elif user["role"] == "student":
        sidebar.pack_forget()
        show_student_dashboard(user)


def show_login_page():
    global login_frame

    sidebar.pack_forget()
    main_area.pack_forget()

    login_frame = tk.Frame(root, bg=BG)
    login_frame.pack(fill="both", expand=True)

    login_card = tk.Frame(
        login_frame,
        bg=WHITE,
        padx=45,
        pady=40,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    login_card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        login_card,
        text="EduStack",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 27, "bold")
    ).pack(pady=(0, 5))

    tk.Label(
        login_card,
        text="SCHOOL MANAGEMENT SYSTEM",
        bg=WHITE,
        fg=BLUE,
        font=("Segoe UI", 9, "bold")
    ).pack(pady=(0, 25))

    tk.Label(
        login_card,
        text="Welcome Back",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 17, "bold")
    ).pack(anchor="w")

    tk.Label(
        login_card,
        text="Sign in to access your school dashboard.",
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(anchor="w", pady=(5, 20))

    tk.Label(
        login_card,
        text="Username / ID",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w")

    username_entry = tk.Entry(
        login_card,
        width=38,
        font=("Segoe UI", 11),
        relief="solid",
        bd=1
    )
    username_entry.pack(pady=(7, 16), ipady=9)

    tk.Label(
        login_card,
        text="Password",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w")

    password_entry = tk.Entry(
        login_card,
        width=38,
        show="*",
        font=("Segoe UI", 11),
        relief="solid",
        bd=1
    )
    password_entry.pack(pady=(7, 20), ipady=9)

    tk.Button(
        login_card,
        text="Sign In",
        command=lambda: handle_login(
            username_entry,
            password_entry
        ),
        bg=BLUE,
        fg=WHITE,
        activebackground=NAVY,
        activeforeground=WHITE,
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=12,
        cursor="hand2"
    ).pack(fill="x")

    tk.Label(
        login_card,
        text="EduStack | School Management",
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 8)
    ).pack(pady=(22, 0))

    username_entry.focus_set()

    # Press Enter to log in
    password_entry.bind(
        "<Return>",
        lambda event: handle_login(
            username_entry,
            password_entry
        )
    )


# -------------------- START APPLICATION --------------------

show_login_page()
root.mainloop()
