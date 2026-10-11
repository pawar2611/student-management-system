
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


# Create database and table
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                course TEXT NOT NULL
            )
        """)


# Home page: display students
@app.route("/")
def index():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        students = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

    return render_template("index.html", students=students)


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        roll = request.form["roll"].strip()
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        course = request.form["course"].strip()

        with sqlite3.connect(DATABASE) as conn:
            conn.execute("""
                INSERT INTO students (roll, name, email, course)
                VALUES (?, ?, ?, ?)
            """, (roll, name, email, course))

        return redirect(url_for("index"))

    return render_template("form.html", student=None)


# Edit student
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

    if student is None:
        return "Student not found", 404

    if request.method == "POST":
        roll = request.form["roll"].strip()
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        course = request.form["course"].strip()

        with sqlite3.connect(DATABASE) as conn:
            conn.execute("""
                UPDATE students
                SET roll = ?, name = ?, email = ?, course = ?
                WHERE id = ?
            """, (roll, name, email, course, student_id))

        return redirect(url_for("index"))

    return render_template("form.html", student=student)


# Delete student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
