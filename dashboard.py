from tkinter import *
from tkinter import messagebox
from result import Result
import sqlite3
from student import Student
from course import CourseClass
from result import Result
from view_result import ReportClass

# In files ko baad me banayenge
# from course import CourseClass
# from student import StudentClass
# from result import ResultClass
# from view_result import ReportClass


class Dashboard:
    def open_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = Result(self.new_win)
    def open_student(self):
        Toplevel(self.root)
        Student(Toplevel(self.root))


    def open_course(self):
        Toplevel(self.root)
        CourseClass(Toplevel(self.root))


    def open_result(self):
        Toplevel(self.root)
        Result(Toplevel(self.root))


    def open_view_result(self):
        Toplevel(self.root)
        ReportClass(Toplevel(self.root))
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#f4f7fc")
        self.root.resizable(False, False)

        # ===================== Title =====================
        title = Label(
            self.root,
            text="Student Result Management System",
            font=("Segoe UI", 24, "bold"),
            bg="#0b5377",
            fg="white",
            pady=10
        )
        title.pack(fill=X)

        # ===================== Menu =====================
        menu_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        menu_frame.place(x=10, y=70, width=1330, height=70)
        #self.student_img = PhotoImage(file="images/student.png")
        #self.course_img = PhotoImage(file="images/course.png")
        #self.result_img = PhotoImage(file="images/result.png")

        Button(
            menu_frame,
            text="Course",
            font=("Segoe UI", 12, "bold"),
            bg="#0b5377",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.open_course
            #image=self.course_img

        ).grid(row=0, column=0, padx=10, pady=12)

        Button(
            menu_frame,
            text="Student",
            font=("Segoe UI", 12, "bold"),
            bg="#0b5377",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.open_student
            #image=self.student_img
        ).grid(row=0, column=1, padx=10)

        Button(
            menu_frame,
            text="Result",
            font=("Segoe UI", 12, "bold"),
            bg="#0b5377",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.open_result
            #image=self.result_img
        ).grid(row=0, column=2, padx=10)
        

        Button(
            menu_frame,
            text="View Result",
            font=("Segoe UI", 12, "bold"),
            bg="#0b5377",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.open_view_result
        ).grid(row=0, column=3, padx=10)

        Button(
            menu_frame,
            text="Logout",
            font=("Segoe UI", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.logout
        ).grid(row=0, column=4, padx=10)

        Button(
            menu_frame,
            text="Exit",
            font=("Segoe UI", 12, "bold"),
            bg="#2c3e50",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.exit_app
        ).grid(row=0, column=5, padx=10)
        #menu_frame.place(relx=0.5, y=90, anchor="n")

        # ===================== Welcome =====================
        Label(
            self.root,
            text="Welcome Admin",
            font=("Segoe UI", 26, "bold"),
            bg="#f4f7fc",
            fg="#0b5377"
        ).place(x=470, y=180)

        Label(
            self.root,
            text="Professional Student Result Management System",
            font=("Segoe UI", 16),
            bg="#f4f7fc",
            fg="gray"
        ).place(x=400, y=230)

        # ===================== Cards =====================
        self.lbl_course = Label(
            self.root,
            text="Courses\n0",
            font=("Segoe UI", 18, "bold"),
            bg="#16a085",
            fg="white"
        )
        self.lbl_course.place(x=180, y=330, width=220, height=120)

        self.lbl_student = Label(
            self.root,
            text="Students\n0",
            font=("Segoe UI", 18, "bold"),
            bg="#2980b9",
            fg="white"
        )
        self.lbl_student.place(x=430, y=330, width=220, height=120)

        self.lbl_result = Label(
            self.root,
            text="Results\n0",
            font=("Segoe UI", 18, "bold"),
            bg="#8e44ad",
            fg="white"
        )
        self.lbl_result.place(x=680, y=330, width=220, height=120)

        # Footer
        footer = Label(
            self.root,
            text="Student Result Management System | Developed by Utkarsh pandey contact No-9721025689",
            font=("Segoe UI", 11),
            bg="#0b5377",
            fg="white"
        )
        footer.pack(side=BOTTOM, fill=X)
        self.update_dashboard()

    def logout(self):
        self.root.destroy()

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.root.destroy()
        # ================= Dashboard Count =================
    def update_dashboard(self):
        con = sqlite3.connect("srms.db")
        cur = con.cursor()

        # Course Count
        try:
            cur.execute("SELECT * FROM course")
            course = len(cur.fetchall())
            self.lbl_course.config(text=f"Courses\n{course}")
        except:
            self.lbl_course.config(text="Courses\n0")

        # Student Count
        try:
            cur.execute("SELECT * FROM student")
            student = len(cur.fetchall())
            self.lbl_student.config(text=f"Students\n{student}")
        except:
            self.lbl_student.config(text="Students\n0")

        # Result Count
        try:
            cur.execute("SELECT * FROM result")
            result = len(cur.fetchall())
            self.lbl_result.config(text=f"Results\n{result}")
        except:
            self.lbl_result.config(text="Results\n0")

        con.close()

        # Auto Refresh Every 2 Seconds
        self.root.after(2000, self.update_dashboard)

    # ================= Open Windows =================
    def open_course(self):
        from course import CourseClass
        new_win = Toplevel(self.root)
        CourseClass(new_win)

    def open_student(self):
        from student import StudentClass
        new_win = Toplevel(self.root)
        StudentClass(new_win)

    def open_result(self):
        from result import ResultClass
        new_win = Toplevel(self.root)
        ResultClass(new_win)

    def open_view_result(self):
        from view_result import ReportClass
        new_win = Toplevel(self.root)
        ReportClass(new_win)
root = Tk()
obj = Dashboard(root)
root.mainloop()