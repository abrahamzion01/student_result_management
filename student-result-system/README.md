# ZAIEON Schools

### Empowering Schools. Developing Futures.

ZAIEON Schools is a Python-based school management desktop application designed to help primary and secondary schools manage student information, academic results, teacher assignments and essential school operations.

The project is being developed with a focus on simplifying school administration, improving academic record management and creating a connected digital environment for schools.

## Current Features

- Student registration and record management.
- Student identification using unique registration numbers.
- Examination score entry and validation.
- Automatic calculation of total and average scores.
- Automatic grade assignment.
- Individual student result viewing.
- Student search functionality.
- Best and lowest performing student identification.
- Administrator, teacher and student authentication.
- Teacher class assignment.
- Class-based attendance management.
- Persistent data storage.

## School Structure

The system supports the Nigerian primary and secondary school structure:

- Primary 1–6
- JSS 1–3
- SS 1–3

## User Roles

**Administrator**
- Manage school operations.
- Manage student records.
- Manage teacher accounts and class assignments.

**Teacher**
- Access assigned classes.
- Support academic and attendance management.

**Student**
- Access personal academic information and relevant school records.

## Technologies

- Python 3
- Tkinter – Desktop graphical user interface.
- SQLite – Database management.
- JSON – Student record storage.
- Pytest – Automated testing.

## Project Structure

```text
student-result-system/
│
├── gui.py
├── database.py
├── students.json
├── test_authentication.py
├── backup/
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Enter the project directory

```bash
cd student-result-system
```

### 3. Run the application

```bash
python gui.py
```

Python 3 is required. Tkinter is also required for the graphical interface.

## Project Vision