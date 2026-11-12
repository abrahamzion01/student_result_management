
import json
import os

students = []

SUBJECTS = ["Mathematics", "English", "Biology"]
DATABASE_FILE = "students.json"


# Load student records from JSON
def load_students():
    global students

    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r") as file:
                students = json.load(file)
        except (json.JSONDecodeError, OSError):
            students = []
    else:
        students = []


# Save student records to JSON
def save_students():
    with open(DATABASE_FILE, "w") as file:
        json.dump(students, file, indent=4)


# Register a student
def register_student():
    name = input("Enter student name: ").strip()
    registration_number = input("Enter registration number: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    if not registration_number:
        print("Registration number cannot be empty!")
        return

    for student in students:
        if student["reg_no"].lower() == registration_number.lower():
            print("Registration number already exists!")
            return

    student = {
        "name": name,
        "reg_no": registration_number,
        "subjects": {},
        "total": None,
        "average": None,
        "grade": None
    }

    students.append(student)
    save_students()

    print("Student registered successfully!")


# Calculate grade
def calculate_grade(average):
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 45:
        return "D"
    elif average >= 40:
        return "E"
    else:
        return "F"


# Enter student scores
def enter_scores():
    registration_number = input(
        "Enter student registration number: "
    ).strip()

    found_student = None

    for student in students:
        if student["reg_no"].lower() == registration_number.lower():
            found_student = student
            break

    if found_student is None:
        print("Student not found!")
        return

    scores = {}

    for subject in SUBJECTS:
        while True:
            try:
                score = float(input(f"Enter {subject} score: "))

                if 0 <= score <= 100:
                    scores[subject] = score
                    break
                else:
                    print("Score must be between 0 and 100!")

            except ValueError:
                print("Please enter a valid number!")

    total = sum(scores.values())
    average = total / len(SUBJECTS)
    grade = calculate_grade(average)

    found_student["subjects"] = scores
    found_student["total"] = total
    found_student["average"] = average
    found_student["grade"] = grade

    save_students()

    print("Scores recorded successfully!")


# Display an individual student result
def display_result(student):
    print("\n========== STUDENT RESULT ==========")
    print(f"Name: {student['name']}")
    print(f"Registration Number: {student['reg_no']}")

    if student["average"] is None:
        print("Scores have not been entered yet.")
        return

    print("\nSubject Scores:")

    for subject, score in student["subjects"].items():
        print(f"{subject}: {score:g}")

    print(f"\nTotal Score: {student['total']:g}")
    print(f"Average Score: {student['average']:.2f}")
    print(f"Grade: {student['grade']}")
    print("====================================")


# View individual result
def view_result():
    registration_number = input(
        "Enter registration number: "
    ).strip()

    for student in students:
        if student["reg_no"].lower() == registration_number.lower():
            display_result(student)
            return

    print("Student not found!")


# View all student results
def view_all_results():
    if not students:
        print("No students registered yet!")
        return

    for student in students:
        display_result(student)


# Search for a student
def search_student():
    registration_number = input(
        "Enter registration number to search: "
    ).strip()

    for student in students:
        if student["reg_no"].lower() == registration_number.lower():
            print("\nStudent found!")
            print(f"Name: {student['name']}")
            print(f"Registration Number: {student['reg_no']}")
            return

    print("Student not found!")


# Find best performing student
def best_student():
    scored_students = [
        student for student in students
        if student["average"] is not None
    ]

    if not scored_students:
        print("No student results available!")
        return

    best = max(scored_students, key=lambda student: student["average"])

    print("\n===== BEST PERFORMING STUDENT =====")
    display_result(best)


# Find lowest performing student
def lowest_student():
    scored_students = [
        student for student in students
        if student["average"] is not None
    ]

    if not scored_students:
        print("No student results available!")
        return

    lowest = min(scored_students, key=lambda student: student["average"])

    print("\n===== LOWEST PERFORMING STUDENT =====")
    display_result(lowest)


# Main menu
def main():
    load_students()

    while True:
        print("\n===== STUDENT RESULT MANAGEMENT =====")
        print("1. Register Student")
        print("2. Enter Student Scores")
        print("3. View Student Result")
        print("4. View All Results")
        print("5. Search Student")
        print("6. View Best Performing Student")
        print("7. View Lowest Performing Student")
        print("8. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            register_student()

        elif choice == "2":
            enter_scores()

        elif choice == "3":
            view_result()

        elif choice == "4":
            view_all_results()

        elif choice == "5":
            search_student()

        elif choice == "6":
            best_student()

        elif choice == "7":
            lowest_student()

        elif choice == "8":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice! Please select 1-8.")


if __name__ == "__main__":
    main()
