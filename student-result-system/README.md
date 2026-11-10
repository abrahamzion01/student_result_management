# Student Result Management System

## Project Overview

The Student Result Management System is a Python-based terminal application designed to help an administrator manage student records and examination results.

The application allows administrators to register students, enter examination scores for three subjects, calculate total and average scores, automatically assign grades, and view student performance.

Student records are stored in a JSON file to ensure that data remains available even after the application is closed.

## Features

- Register students with their full names and unique matriculation numbers.
- Prevent duplicate matriculation numbers.
- Enter examination scores in three subjects:
  - Mathematics
  - English
  - Biology
- Validate scores to ensure they are between 0 and 100.
- Automatically calculate total scores.
- Calculate average scores.
- Automatically assign grades.
- View individual student results.
- Display all registered students and their results.
- Search for students using matriculation numbers.
- Identify the best-performing student.
- Identify the lowest-performing student.
- Store student records in a JSON database.
- Preserve student records after restarting the application.
- Handle invalid user inputs.

## Grading System

The application uses the following grading scale:

| Average Score | Grade |
|---|---|
| 70–100 | A |
| 60–69 | B |
| 50–59 | C |
| 45–49 | D |
| 40–44 | E |
| 0–39 | F |

## How Calculations Work

### Total Score

The total score is calculated by adding the scores from the three subjects.

`Total = Mathematics + English + Biology`

### Average Score

The average score is calculated by dividing the total score by the number of subjects.

`Average = Total Score / 3`

### Grade Assignment

The system uses conditional statements (`if`, `elif`, and `else`) to compare the student's average score against the grading scale and automatically assign the appropriate grade.

## Technologies Used

- Python 3
- JSON for data storage
- Python standard library
- Ubuntu/Linux terminal

## Project Structure

```text
student-result-system/
│
├── main.py
├── students.json
└── README.md
```

### File Description

- `main.py`: Contains the application logic, functions, calculations, validation and terminal menu.
- `students.json`: Stores registered students, examination scores and calculated results.
- `README.md`: Provides project documentation and usage instructions.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate into the project directory

```bash
cd student-result-system
```

### 3. Run the application

```bash
python3 main.py
```

No external Python libraries are required.

## Application Menu

When the application starts, the following menu is displayed:

```text
===== STUDENT RESULT MANAGEMENT =====

1. Register Student
2. Enter Student Scores
3. View Student Result
4. View All Results
5. Search Student
6. View Best Performing Student
7. View Lowest Performing Student
8. Exit

Choose an option:
```

## Sample Demonstration

The system was tested with five sample students:

| Student | Matriculation Number | Average | Grade |
|---|---|---:|---|
| Emmanuel Odeh | STU001 | 65.67 | B |
| John Ikwube | STU002 | 44.00 | E |
| Nese Girinya | STU003 | 40.00 | E |
| Onyeke Benedict | STU004 | 27.33 | F |
| Kingsley Exenaia | STU005 | 64.00 | B |

**Best-performing student:** Emmanuel Odeh

**Lowest-performing student:** Onyeke Benedict

## Data Storage

Student information is stored in `students.json`.

The application uses Python's built-in `json` module to save and retrieve student records.

This ensures that registered students and their results remain available after restarting the application.

## Future Improvements

Possible future improvements include:

- Adding more subjects.
- Editing existing student records.
- Deleting student records.
- Generating printable result reports.
- Adding an SQLite database.
- Developing a graphical or web-based interface.

## Author

Developed as a Python programming terminal project.

## License

This project is intended for educational and learning purposes.