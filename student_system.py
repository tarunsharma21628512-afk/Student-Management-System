# ==============================
# STUDENT MANAGEMENT SYSTEM
# Developed By: Tarun Sharma
# Tech Used: Python + MySQL
# ==============================

import mysql.connector

# ------------------------------
# DATABASE CONNECTION
# ------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="student_system"
    )
    cursor = conn.cursor()
    print("Database Connected Successfully!")
except:
    print("Database Connection Failed!")
    exit()

# ------------------------------
# CREATE TABLES IF NOT EXISTS
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    course VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject1 INT,
    subject2 INT,
    subject3 INT,
    total INT,
    percentage FLOAT,
    grade VARCHAR(5),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
""")

conn.commit()

# ------------------------------
# GRADE CALCULATION
# ------------------------------
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 75:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "Fail"

# ------------------------------
# ADD STUDENT
# ------------------------------
def add_student():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    course = input("Enter Course: ")

    query = "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)"
    values = (name, age, course)

    cursor.execute(query, values)
    conn.commit()

    print("Student Added Successfully!")

# ------------------------------
# ADD MARKS
# ------------------------------
def add_marks():
    student_id = int(input("Enter Student ID: "))
    s1 = int(input("Enter Subject1 Marks: "))
    s2 = int(input("Enter Subject2 Marks: "))
    s3 = int(input("Enter Subject3 Marks: "))

    total = s1 + s2 + s3
    percentage = total / 3
    grade = calculate_grade(percentage)

    query = """INSERT INTO marks 
               (student_id, subject1, subject2, subject3, total, percentage, grade)
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    values = (student_id, s1, s2, s3, total, percentage, grade)

    cursor.execute(query, values)
    conn.commit()

    print("Marks Added Successfully!")

# ------------------------------
# VIEW REPORT
# ------------------------------
def view_report():
    student_id = int(input("Enter Student ID: "))

    query = """
    SELECT students.name, students.course,
           marks.subject1, marks.subject2, marks.subject3,
           marks.total, marks.percentage, marks.grade
    FROM students
    JOIN marks ON students.student_id = marks.student_id
    WHERE students.student_id = %s
    """

    cursor.execute(query, (student_id,))
    result = cursor.fetchone()

    if result:
        print("\n----- STUDENT REPORT -----")
        print("Name:", result[0])
        print("Course:", result[1])
        print("Subject1:", result[2])
        print("Subject2:", result[3])
        print("Subject3:", result[4])
        print("Total:", result[5])
        print("Percentage:", result[6])
        print("Grade:", result[7])
    else:
        print("No record found.")

# ------------------------------
# SHOW TOPPER
# ------------------------------
def show_topper():
    query = """
    SELECT students.name, MAX(marks.percentage)
    FROM students
    JOIN marks ON students.student_id = marks.student_id
    """

    cursor.execute(query)
    result = cursor.fetchone()

    if result and result[0]:
        print("\nTopper Name:", result[0])
        print("Highest Percentage:", result[1])
    else:
        print("No data available.")

# ------------------------------
# MAIN MENU
# ------------------------------
while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. Add Marks")
    print("3. View Report")
    print("4. Show Topper")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_student()
    elif choice == '2':
        add_marks()
    elif choice == '3':
        view_report()
    elif choice == '4':
        show_topper()
    elif choice == '5':
        print("Exiting System...")
        break
    else:
        print("Invalid Choice!")

# Close connection
conn.close()
