import sqlite3


def create_db():
    con = sqlite3.connect("srms.db")
    cur = con.cursor()

    # Course Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS course(
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        duration TEXT,
        charges TEXT,
        description TEXT
    )
    """)

    # Student Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student(
        roll TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        gender TEXT,
        dob TEXT,
        contact TEXT,
        admission TEXT,
        course TEXT,
        state TEXT,
        city TEXT,
        pin TEXT,
        address TEXT
    )
    """)

    # Result Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS result(
        rid INTEGER PRIMARY KEY AUTOINCREMENT,
        roll TEXT,
        name TEXT,
        course TEXT,
        marks_obtained INTEGER,
        full_marks INTEGER,
        percentage REAL,
        grade TEXT
    )
    """)

    con.commit()
    con.close()


if __name__ == "__main__":
    create_db()
    print("Database Created Successfully")