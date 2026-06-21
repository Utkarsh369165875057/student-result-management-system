import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class ReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("View Result")
        self.root.geometry("800x400")

        # ================= TITLE =================
        Label(self.root, text="RESULT RECORDS",
              font=("Arial", 18, "bold"), bg="blue", fg="white").pack(fill=X)

        # ================= TABLE =================
        frame = Frame(self.root)
        frame.pack(fill=BOTH, expand=1)

        scroll = Scrollbar(frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(frame,
                                  columns=("roll", "name", "course", "marks", "percent", "grade"),
                                  yscrollcommand=scroll.set)

        scroll.config(command=self.table.yview)

        self.table.heading("roll", text="Roll")
        self.table.heading("name", text="Name")
        self.table.heading("course", text="Course")
        self.table.heading("marks", text="Marks")
        self.table.heading("percent", text="Percent")
        self.table.heading("grade", text="Grade")

        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)

        self.show_data()

    def show_data(self):
        conn = sqlite3.connect("rms.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM result")
        rows = cur.fetchall()

        conn.close()

        self.table.delete(*self.table.get_children())

        for row in rows:
            self.table.insert("", END, values=row)