from tkinter import *
from tkinter import messagebox
from dashboard import Dashboard
from dashboard import Dashboard
from tkinter import Toplevel

def open_dashboard(self):
    self.new_win = Toplevel(self.root)
    Dashboard(self.new_win)


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#f4f7fc")
        self.root.resizable(False, False)

        # ================= Title =================
        title = Label(
            self.root,
            text="Student Result Management System",
            font=("Segoe UI", 26, "bold"),
            bg="#0b5377",
            fg="white",
            pady=15
        )
        title.pack(fill=X)

        # ================= Login Frame =================
        login_frame = Frame(
            self.root,
            bg="white",
            bd=3,
            relief=RIDGE
        )
        login_frame.place(x=450, y=160, width=450, height=350)

        Label(
            login_frame,
            text="Admin Login",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#0b5377"
        ).pack(pady=20)

        Label(
            login_frame,
            text="Username",
            font=("Segoe UI", 13),
            bg="white"
        ).place(x=50, y=90)

        self.username = Entry(
            login_frame,
            font=("Segoe UI", 13)
        )
        self.username.place(x=50, y=120, width=340)

        Label(
            login_frame,
            text="Password",
            font=("Segoe UI", 13),
            bg="white"
        ).place(x=50, y=170)

        self.password = Entry(
            login_frame,
            show="*",
            font=("Segoe UI", 13)
        )
        self.password.place(x=50, y=200, width=340)

        Button(
            login_frame,
            text="LOGIN",
            font=("Segoe UI", 13, "bold"),
            bg="#0b5377",
            fg="white",
            cursor="hand2",
            command=self.login
        ).place(x=130, y=270, width=180, height=40)

    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)

        elif self.username.get() == "admin" and self.password.get() == "admin123":
            self.new_window = Toplevel(self.root)
            self.app = Dashboard(self.new_window)
            self.root.withdraw()

        else:
            messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)