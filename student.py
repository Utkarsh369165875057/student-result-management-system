import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("900x500")

        # ================= VARIABLES =================
        self.roll_var = StringVar()
        self.name_var = StringVar()
        self.course_var = StringVar()
        self.marks_var = StringVar()

        # ================= DATABASE =================
        self.create_db()

        # ================= TITLE =================
        title = Label(root, text="Student Result Management System",
                      font=("Arial", 20, "bold"), bg="blue", fg="white")
        title.pack(side=TOP, fill=X)

    def create_db(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll TEXT PRIMARY KEY,
            name TEXT,
            course TEXT,
            marks TEXT
        )
        """)

        conn.commit()
        conn.close()
                # ================= FRAME =================
        form = Frame(self.root, bd=2, relief=RIDGE)
        form.place(x=20, y=60, width=350, height=400)

        # Roll
        Label(form, text="Roll No").grid(row=0, column=0, pady=10, padx=10, sticky=W)
        Entry(form, textvariable=self.roll_var).grid(row=0, column=1)

        # Name
        Label(form, text="Name").grid(row=1, column=0, pady=10, padx=10, sticky=W)
        Entry(form, textvariable=self.name_var).grid(row=1, column=1)

        # Course
        Label(form, text="Course").grid(row=2, column=0, pady=10, padx=10, sticky=W)
        Entry(form, textvariable=self.course_var).grid(row=2, column=1)

        # Marks
        Label(form, text="Marks").grid(row=3, column=0, pady=10, padx=10, sticky=W)
        Entry(form, textvariable=self.marks_var).grid(row=3, column=1)

        # Buttons
        Button(form, text="Add", command=self.add).grid(row=4, column=0, pady=20)
        Button(form, text="Update", command=self.update).grid(row=4, column=1)
        Button(form, text="Delete", command=self.delete).grid(row=5, column=0)
        Button(form, text="Clear", command=self.clear).grid(row=5, column=1)
        Button(form, text="Search", command=self.search).grid(row=6, column=0, columnspan=2)
                # ================= TABLE =================
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.place(x=400, y=60, width=470, height=400)

        scroll = Scrollbar(table_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("roll", "name", "course", "marks"),
            yscrollcommand=scroll.set
        )

        scroll.config(command=self.student_table.yview)

        self.student_table.heading("roll", text="Roll")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("marks", text="Marks")

        self.student_table["show"] = "headings"

        self.student_table.pack(fill=BOTH, expand=1)

        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.show()
    def add(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO student VALUES (?, ?, ?, ?)",
                        (self.roll_var.get(),
                         self.name_var.get(),
                         self.course_var.get(),
                         self.marks_var.get()))
            conn.commit()
            messagebox.showinfo("Success", "Student Added")
        except:
            messagebox.showerror("Error", "Roll already exists")

        conn.close()
        self.show()
        self.clear()

    def show(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        conn.close()

        self.student_table.delete(*self.student_table.get_children())

        for row in rows:
            self.student_table.insert("", END, values=row)

    def delete(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM student WHERE roll=?",
                    (self.roll_var.get(),))

        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Record Deleted")
        self.show()
        self.clear()

    def update(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("""
        UPDATE student 
        SET name=?, course=?, marks=? 
        WHERE roll=?
        """, (
            self.name_var.get(),
            self.course_var.get(),
            self.marks_var.get(),
            self.roll_var.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Record Updated")
        self.show()

    def search(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM student WHERE roll=?",
                    (self.roll_var.get(),))

        row = cur.fetchone()
        conn.close()

        self.student_table.delete(*self.student_table.get_children())

        if row:
            self.student_table.insert("", END, values=row)
        else:
            messagebox.showerror("Error", "Not Found")

    def clear(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.course_var.set("")
        self.marks_var.set("")

    def get_cursor(self, event):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content["values"]

        if row:
            self.roll_var.set(row[0])
            self.name_var.set(row[1])
            self.course_var.set(row[2])
            self.marks_var.set(row[3])
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
