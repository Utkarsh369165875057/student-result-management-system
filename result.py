import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class Result:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")
        self.root.geometry("900x500")

        # ================= VARIABLES =================
        self.roll_var = StringVar()
        self.name_var = StringVar()
        self.course_var = StringVar()
        self.marks_var = StringVar()

        # ================= TITLE =================
        title = Label(self.root, text="Result Management System",
                      font=("Arial", 20, "bold"), bg="green", fg="white")
        title.pack(side=TOP, fill=X)

        # ================= FORM =================
        form = Frame(self.root, bd=2, relief=RIDGE)
        form.place(x=20, y=60, width=350, height=400)

        Label(form, text="Roll No").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        Entry(form, textvariable=self.roll_var).grid(row=0, column=1)

        Label(form, text="Name").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        Entry(form, textvariable=self.name_var).grid(row=1, column=1)

        Label(form, text="Course").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        Entry(form, textvariable=self.course_var).grid(row=2, column=1)

        Label(form, text="Marks").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        Entry(form, textvariable=self.marks_var).grid(row=3, column=1)

        Button(form, text="Calculate", command=self.calculate).grid(row=4, column=0, pady=20)
        Button(form, text="Save", command=self.save).grid(row=4, column=1)
        Button(form, text="Clear", command=self.clear).grid(row=5, column=0, columnspan=2)
        Button(form, text="View Result", command=self.view_result).grid(row=6, column=0, columnspan=2, pady=10)

        # ================= TABLE =================
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.place(x=400, y=60, width=470, height=400)

        scroll = Scrollbar(table_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(table_frame,
                                  columns=("roll", "name", "course", "marks", "percent", "grade"),
                                  yscrollcommand=scroll.set)

        scroll.config(command=self.table.yview)

        self.table.heading("roll", text="Roll")
        self.table.heading("name", text="Name")
        self.table.heading("course", text="Course")
        self.table.heading("marks", text="Marks")
        self.table.heading("percent", text="Percentage")
        self.table.heading("grade", text="Grade")

        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)

        self.show()

    # ================= CALCULATE =================
    def calculate(self):
        try:
            marks = float(self.marks_var.get())
            percent = (marks / 100) * 100  # assume out of 100

            if percent >= 90:
                grade = "A+"
            elif percent >= 75:
                grade = "A"
            elif percent >= 60:
                grade = "B"
            elif percent >= 40:
                grade = "C"
            else:
                grade = "Fail"

            self.percent = percent
            self.grade = grade

            messagebox.showinfo("Result", f"Percentage: {percent}\nGrade: {grade}")

        except:
            messagebox.showerror("Error", "Invalid Marks")

    # ================= SAVE =================
    def save(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        try:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS result(
                roll TEXT,
                name TEXT,
                course TEXT,
                marks TEXT,
                percent TEXT,
                grade TEXT
            )
            """)

            cur.execute("INSERT INTO result VALUES (?, ?, ?, ?, ?, ?)",
                        (self.roll_var.get(),
                         self.name_var.get(),
                         self.course_var.get(),
                         self.marks_var.get(),
                         str(getattr(self, "percent", "")),
                         getattr(self, "grade", "")))

            conn.commit()
            messagebox.showinfo("Success", "Result Saved")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        conn.close()
        self.show()

    # ================= SHOW =================
    def show(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM result")
        rows = cur.fetchall()

        conn.close()

        self.table.delete(*self.table.get_children())

        for row in rows:
            self.table.insert("", END, values=row)

    # ================= CLEAR =================
    def clear(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.course_var.set("")
        self.marks_var.set("")
    def view_result(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM result WHERE roll=?", (self.roll_var.get(),))
        row = cur.fetchone()

        conn.close()

        self.table.delete(*self.table.get_children())

        if row:
            self.table.insert("", END, values=row)
            messagebox.showinfo("Success", "Result Found")
        else:
            messagebox.showerror("Error", "No Result Found")


# ================= RUN =================
if __name__ == "__main__":
    root = Tk()
    obj = Result(root)
    root.mainloop()