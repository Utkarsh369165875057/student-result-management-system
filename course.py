from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Management")
        self.root.geometry("1200x600+80+80")
        self.root.config(bg="white")
        self.root.focus_force()

        # ================= Variables =================
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()

        # ================= Title =================
        title = Label(
            self.root,
            text="Manage Course Details",
            font=("Segoe UI", 20, "bold"),
            bg="#033054",
            fg="white"
        )
        title.pack(fill=X)

        # ================= Labels =================
        Label(
            self.root,
            text="Course Name",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).place(x=30, y=80)

        self.txt_course = Entry(
            self.root,
            textvariable=self.var_course,
            font=("Segoe UI", 13),
            bd=2,
            relief=GROOVE
        )
        self.txt_course.place(x=30, y=115, width=350)

        Label(
            self.root,
            text="Duration",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).place(x=30, y=170)

        self.txt_duration = Entry(
            self.root,
            textvariable=self.var_duration,
            font=("Segoe UI", 13),
            bd=2,
            relief=GROOVE
        )
        self.txt_duration.place(x=30, y=205, width=350)

        Label(
            self.root,
            text="Charges",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).place(x=30, y=260)

        self.txt_charges = Entry(
            self.root,
            textvariable=self.var_charges,
            font=("Segoe UI", 13),
            bd=2,
            relief=GROOVE
        )
        self.txt_charges.place(x=30, y=295, width=350)

        Label(
            self.root,
            text="Description",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).place(x=30, y=350)

        self.txt_description = Text(
            self.root,
            font=("Segoe UI", 12),
            bd=2,
            relief=GROOVE
        )
        self.txt_description.place(x=30, y=385, width=350, height=120)

        # ================= Buttons =================
        Button(
            self.root,
            text="Save",
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            cursor="hand2",
            command=self.add
        ).place(x=30, y=530, width=80)

        Button(
            self.root,
            text="Update",
            font=("Segoe UI", 12, "bold"),
            bg="#007bff",
            fg="white",
            cursor="hand2",
            command=self.update
        ).place(x=120, y=530, width=80)

        Button(
            self.root,
            text="Delete",
            font=("Segoe UI", 12, "bold"),
            bg="#dc3545",
            fg="white",
            cursor="hand2",
            command=self.delete
        ).place(x=210, y=530, width=80)

        Button(
            self.root,
            text="Clear",
            font=("Segoe UI", 12, "bold"),
            bg="#6c757d",
            fg="white",
            cursor="hand2",
            command=self.clear
        ).place(x=300, y=530, width=80)

        # ================= Course List =================
        self.course_list = Listbox(
            self.root,
            font=("Segoe UI", 12),
            bd=2,
            relief=GROOVE
        )
        self.course_list.place(x=450, y=80, width=700, height=450)

        scrollbar = Scrollbar(self.course_list)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.course_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.course_list.yview)

        self.course_list.bind("<ButtonRelease-1>", self.get_data)

        self.show()
        # ================= Save Course =================
    def add(self):
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Course Name is required", parent=self.root)
            return

        con = sqlite3.connect("srms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror("Error", "Course already exists", parent=self.root)
            else:
                cur.execute(
                    "INSERT INTO course(name,duration,charges,description) VALUES(?,?,?,?)",
                    (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END),
                    ),
                )
                con.commit()
                messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                self.show()
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error : {str(ex)}", parent=self.root)

        finally:
            con.close()

    # ================= Show Courses =================
    def show(self):
        con = sqlite3.connect("srms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()

            self.course_list.delete(0, END)

            for row in rows:
                self.course_list.insert(END, row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error : {str(ex)}", parent=self.root)

        finally:
            con.close()

    # ================= Get Selected Course =================
    def get_data(self, ev):
        try:
            index = self.course_list.curselection()[0]
            row = self.course_list.get(index)

            self.var_course.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])

            self.txt_description.delete("1.0", END)
            self.txt_description.insert(END, row[4])

        except:
            pass
        # ================= Update Course =================
    def update(self):
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Please select a course first", parent=self.root)
            return

        con = sqlite3.connect("srms.db")
        cur = con.cursor()

        try:
            cur.execute(
                """UPDATE course SET duration=?, charges=?, description=?
                   WHERE name=?""",
                (
                    self.var_duration.get(),
                    self.var_charges.get(),
                    self.txt_description.get("1.0", END),
                    self.var_course.get()
                )
            )

            con.commit()
            messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error : {str(ex)}", parent=self.root)

        finally:
            con.close()

    # ================= Delete Course =================
    def delete(self):
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Please select a course first", parent=self.root)
            return

        con = sqlite3.connect("srms.db")
        cur = con.cursor()

        try:
            op = messagebox.askyesno(
                "Confirm",
                "Do you really want to delete this course?",
                parent=self.root
            )

            if op:
                cur.execute(
                    "DELETE FROM course WHERE name=?",
                    (self.var_course.get(),)
                )
                con.commit()

                messagebox.showinfo(
                    "Deleted",
                    "Course Deleted Successfully",
                    parent=self.root
                )

                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error : {str(ex)}", parent=self.root)

        finally:
            con.close()

    # ================= Clear =================
    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")

        self.txt_description.delete("1.0", END)

        self.course_list.selection_clear(0, END)

        self.show()