import tkinter as tk
from tkinter import ttk, messagebox
import authentication
import database
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

    class_label = tk.Label(
        panel,
        text="Class",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 10, "bold")
    )
    class_label.pack(anchor="w", pady=(12, 5))

    school_classes = [
        "Primary 1", "Primary 2", "Primary 3",
        "Primary 4", "Primary 5", "Primary 6",
        "JSS 1", "JSS 2", "JSS 3",
        "SS 1", "SS 2", "SS 3"
    ]

    class_dropdown = ttk.Combobox(
        panel,
        values=school_classes,
        state="readonly",
        font=("Segoe UI", 10)
    )
    class_dropdown.pack(fill="x", pady=(0, 10))
    class_dropdown.set("Select class")

    def save_student():
        name = name_entry.get().strip()
        registration = registration_entry.get().strip()
        student_class = class_dropdown.get()

        if not name or not registration or student_class == "Select class":
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
            "class_name": student_class,
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



def show_teacher_classes_admin():
    database.initialize_database()
    clear_page()

    page_heading(
        "Teacher Classes",
        "Assign teachers to their respective classes."
    )

    panel = tk.Frame(page_area, bg=WHITE, padx=25, pady=25)
    panel.pack(fill="x", padx=30, pady=15)

    tk.Label(
        panel, text="Select Teacher",
        bg=WHITE, fg=DARK,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(0, 6))

    teachers = database.get_teachers()
    teacher_options = {
        teacher["username"]: teacher["id"]
        for teacher in teachers
    }

    teacher_var = tk.StringVar()
    teacher_dropdown = ttk.Combobox(
        panel,
        textvariable=teacher_var,
        values=list(teacher_options.keys()),
        state="readonly",
        font=("Segoe UI", 10)
    )
    teacher_dropdown.pack(fill="x", pady=(0, 15))

    tk.Label(
        panel, text="Select Class",
        bg=WHITE, fg=DARK,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(0, 6))

    school_classes = [
        "Primary 1", "Primary 2", "Primary 3",
        "Primary 4", "Primary 5", "Primary 6",
        "JSS 1", "JSS 2", "JSS 3",
        "SS 1", "SS 2", "SS 3"
    ]

    class_var = tk.StringVar()
    class_dropdown = ttk.Combobox(
        panel,
        textvariable=class_var,
        values=school_classes,
        state="readonly",
        font=("Segoe UI", 10)
    )
    class_dropdown.pack(fill="x", pady=(0, 18))

    def assign_class():
        teacher_name = teacher_var.get()
        class_name = class_var.get()

        if not teacher_name or not class_name:
            messagebox.showwarning(
                "Missing Information",
                "Please select a teacher and a class."
            )
            return

        teacher_id = teacher_options[teacher_name]

        success = database.assign_teacher_to_class(
            teacher_id, class_name
        )

        if success:
            messagebox.showinfo(
                "Success",
                f"{class_name} assigned to {teacher_name}."
            )
            refresh_assignments()
        else:
            messagebox.showwarning(
                "Already Assigned",
                "This teacher already has this class assigned."
            )

    make_button(
        panel, "Assign Class", assign_class
    ).pack(anchor="w")

    assignments_panel = tk.Frame(
        page_area, bg=WHITE, padx=25, pady=20
    )
    assignments_panel.pack(
        fill="both", expand=True, padx=30, pady=10
    )

    section_title(
        assignments_panel,
        "Current Teacher Assignments"
    )

    assignment_list = tk.Listbox(
        assignments_panel,
        font=("Segoe UI", 10),
        height=10,
        relief="flat",
        bg="#F7F9FC"
    )
    assignment_list.pack(fill="both", expand=True, pady=10)

    def refresh_assignments():
        assignment_list.delete(0, tk.END)

        connection = database.get_connection()

        rows = connection.execute("""
            SELECT users.username, teacher_classes.class_name
            FROM teacher_classes
            JOIN users ON users.id = teacher_classes.teacher_id
            ORDER BY users.username, teacher_classes.class_name
        """).fetchall()

        connection.close()

        for row in rows:
            assignment_list.insert(
                tk.END,
                f"{row['username']}  —  {row['class_name']}"
            )

        if not rows:
            assignment_list.insert(
                tk.END, "No teacher classes assigned yet."
            )

    refresh_assignments()



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
        "Take Attendance",
        "View Assigned Classes",
        "Monitor Student Attendance",
        "Enter Student Scores",
        "Compile Results"
    ]

    for action in actions:
        tk.Button(
            page_area,
            text=action,
    command=lambda name=action: (
        show_attendance_page(user)
        if name == "Take Attendance"
        else show_attendance_history(user)
        if name == "Monitor Student Attendance"
        else messagebox.showinfo(
            name,
            f"{name} will be connected in the next development stage."
        )
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



def show_attendance_page(user):
    from datetime import date

    clear_page()

    page_heading(
        "Take Attendance",
        "Select a class and record student attendance."
    )

    tk.Button(
    page_area,
    text="← Back to Dashboard",
    command=lambda: show_teacher_dashboard(user),
    bg=WHITE,
    fg=NAVY,
    relief="flat",
    font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=30, pady=5)

    database.initialize_database()

    panel = tk.Frame(page_area, bg=WHITE, padx=25, pady=25)
    panel.pack(fill="both", expand=True, padx=30, pady=20)

    tk.Label(
        panel,
        text="Select Class",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=5)

    school_classes = [
        "Primary 1", "Primary 2", "Primary 3",
        "Primary 4", "Primary 5", "Primary 6",
        "JSS 1", "JSS 2", "JSS 3",
        "SS 1", "SS 2", "SS 3"
    ]

    class_dropdown = ttk.Combobox(
        panel,
        values=school_classes,
        state="readonly"
    )
    class_dropdown.pack(fill="x", pady=10)
    class_dropdown.set("Select class")

    attendance_frame = tk.Frame(panel, bg=WHITE)
    attendance_frame.pack(fill="both", expand=True)

    def load_class_students():
        for widget in attendance_frame.winfo_children():
            widget.destroy()

        selected_class = class_dropdown.get()

        if selected_class == "Select class":
            messagebox.showwarning(
                "Select Class",
                "Please select a class first.",
                parent=root
            )
            return

        class_students = [
            student for student in main.students
            if student.get("class_name") == selected_class
        ]

        if not class_students:
            tk.Label(
                attendance_frame,
                text="No students found in this class.",
                bg=WHITE,
                fg=RED
            ).pack(anchor="w", pady=15)
            return

        tk.Label(
            attendance_frame,
            text=f"Attendance Date: {date.today()}",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=10)

        attendance_entries = []

        for student in class_students:
            row = tk.Frame(attendance_frame, bg=WHITE)
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=f"{student['name']} ({student['reg_no']})",
                bg=WHITE,
                fg=DARK,
                width=30,
                anchor="w"
            ).pack(side="left")

            status = ttk.Combobox(
                row,
                values=["Present", "Absent", "Late"],
                state="readonly",
                width=12
            )
            status.set("Present")
            status.pack(side="right")

            attendance_entries.append((student, status))

        def save_attendance():
            connection = database.get_connection()

            try:
                cursor = connection.cursor()

                for student, status in attendance_entries:
                    cursor.execute("""
                        INSERT INTO attendance (
                            reg_no, class_name,
                            attendance_date, status, marked_by
                        )
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(reg_no, attendance_date)
                        DO UPDATE SET
                            class_name = excluded.class_name,
                            status = excluded.status,
                            marked_by = excluded.marked_by
                    """, (
                        student["reg_no"],
                        selected_class,
                        date.today().isoformat(),
                        status.get(),
                        user["id"]
                    ))

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Attendance saved successfully.",
                    parent=root
                )

            except Exception as error:
                connection.rollback()
                messagebox.showerror(
                    "Attendance Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        tk.Button(
            attendance_frame,
            text="Save Attendance",
            command=save_attendance,
            bg=GREEN,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="w", pady=20)

    tk.Button(
        panel,
        text="Load Students",
        command=load_class_students,
        bg=NAVY,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=20,
        pady=10
    ).pack(anchor="w", pady=10)


def show_attendance_history(user):
    from datetime import date

    clear_page()

    page_heading(
        "Attendance History",
        "View previously recorded student attendance."
    )
    tk.Button(
    page_area,
    text="← Back to Dashboard",
    command=lambda: show_teacher_dashboard(user),
    bg=WHITE,
    fg=NAVY,
    relief="flat",
    font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=30, pady=5)

    database.initialize_database()

    panel = tk.Frame(page_area, bg=WHITE, padx=25, pady=25)
    panel.pack(fill="both", expand=True, padx=30, pady=20)

    school_classes = [
        "Primary 1", "Primary 2", "Primary 3",
        "Primary 4", "Primary 5", "Primary 6",
        "JSS 1", "JSS 2", "JSS 3",
        "SS 1", "SS 2", "SS 3"
    ]

    tk.Label(
        panel,
        text="Select Class",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w")

    class_dropdown = ttk.Combobox(
        panel,
        values=school_classes,
        state="readonly"
    )
    class_dropdown.pack(fill="x", pady=8)
    class_dropdown.set("Select class")

    tk.Label(
        panel,
        text="Attendance Date (YYYY-MM-DD)",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(12, 0))

    date_entry = tk.Entry(panel, font=("Segoe UI", 10))
    date_entry.pack(fill="x", pady=8)
    date_entry.insert(0, date.today().isoformat())

    history_frame = tk.Frame(panel, bg=WHITE)
    history_frame.pack(fill="both", expand=True, pady=15)

    def load_history():
        for widget in history_frame.winfo_children():
            widget.destroy()

        selected_class = class_dropdown.get()
        selected_date = date_entry.get().strip()

        if selected_class == "Select class" or not selected_date:
            messagebox.showwarning(
                "Missing Information",
                "Please select a class and enter a date.",
                parent=root
            )
            return

        try:
            date.fromisoformat(selected_date)
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Enter the date in YYYY-MM-DD format.",
                parent=root
            )
            return

        connection = database.get_connection()

        try:
            records = connection.execute("""
                SELECT
                    attendance.reg_no,
                    attendance.status,
                    attendance.marked_by,
                    users.username AS teacher
                FROM attendance
                LEFT JOIN users
                    ON attendance.marked_by = users.id
                WHERE attendance.class_name = ?
                AND attendance.attendance_date = ?
                ORDER BY attendance.reg_no
            """, (selected_class, selected_date)).fetchall()

        finally:
            connection.close()

        if not records:
            tk.Label(
                history_frame,
                text="No attendance records found for this class and date.",
                bg=WHITE,
                fg=RED
            ).pack(anchor="w", pady=10)
            return

        headings = tk.Frame(history_frame, bg=NAVY)
        headings.pack(fill="x")

        for heading in ("Student Name", "Registration No.", "Status", "Marked By"):
            tk.Label(
                headings,
                text=heading,
                bg=NAVY,
                fg=WHITE,
                font=("Segoe UI", 9, "bold"),
                width=18,
                anchor="w"
            ).pack(side="left", padx=5, pady=8)

        for record in records:
            row = tk.Frame(history_frame, bg=WHITE)
            row.pack(fill="x", pady=3)

            student = next(
                (
                    s for s in main.students
                    if s.get("reg_no", "").lower() == record["reg_no"].lower()
                ),
                None
            )

            student_name = student["name"] if student else "Unknown Student"

            values = (
                student_name,
                record["reg_no"],
                record["status"],
                record["teacher"] or f"User ID {record['marked_by']}"
            )

            for value in values:
                tk.Label(
                    row,
                    text=value,
                    bg=WHITE,
                    fg=DARK,
                    width=18,
                    anchor="w"
                ).pack(side="left", padx=5, pady=5)

        tk.Label(
            history_frame,
            text=f"Total records: {len(records)}",
            bg=WHITE,
            fg=GREEN,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=12)

    tk.Button(
        panel,
        text="View Attendance",
        command=load_history,
        bg=NAVY,
        fg=WHITE,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=10
    ).pack(anchor="w", pady=10)




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
