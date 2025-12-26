import sqlite3
from datetime import date, timedelta, datetime







# ------------------ DB CONNECTION ------------------
connect = sqlite3.connect("new_library.db")
cursor = connect.cursor()
cursor.execute("PRAGMA foreign_keys=ON")
# ------------------ DB CONNECTION ------------------







# ------------------ TABLES ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS student(
    enrollment_no VARCHAR PRIMARY KEY,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS quantity_books(
    book_name_id VARCHAR PRIMARY KEY,
    book_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS all_books(
    book_id VARCHAR PRIMARY KEY,
    book_name_id VARCHAR,
    book_name TEXT NOT NULL,
    is_issued INTEGER DEFAULT 0,
    FOREIGN KEY(book_name_id) REFERENCES quantity_books(book_name_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS published_books(
    enrollment_no VARCHAR,
    book_id VARCHAR UNIQUE,
    book_name_id VARCHAR,
    book_name TEXT NOT NULL,
    issued_date DATE NOT NULL,
    renew_date DATE NOT NULL,
    FOREIGN KEY(enrollment_no) REFERENCES student(enrollment_no),
    FOREIGN KEY(book_id) REFERENCES all_books(book_id),
    FOREIGN KEY(book_name_id) REFERENCES quantity_books(book_name_id)
)
""")
# ------------------ TABLES ------------------








# ------------------ FUNCTIONS ------------------
def show_student_details(enrollment_no):
    cursor.execute(
        "SELECT enrollment_no,name FROM student WHERE enrollment_no=?",
        (enrollment_no,)
    )
    student = cursor.fetchone()

    if not student:
        print("No student found")
        return

    print("\nStudent Details")
    print("Enrollment No:", student[0])
    print("Name:", student[1])

    cursor.execute(
        "SELECT book_name,renew_date FROM published_books WHERE enrollment_no=?",
        (enrollment_no,)
    )

    fine = 0
    for book_name, renew_date in cursor.fetchall():
        renew_date = datetime.strptime(renew_date, "%Y-%m-%d").date()
        overdue = (date.today() - renew_date).days
        if overdue > 0:
            fine += overdue * 10
        print(book_name, renew_date)

    print("Fine amount:", fine)




def issue_book(enrollment_no):
    book_id = input("Enter the book_id: ")

    cursor.execute(
        "SELECT book_name,book_name_id FROM all_books WHERE book_id=? AND is_issued=0",
        (book_id,)
    )
    book = cursor.fetchone()

    if not book:
        print("Book already issued or invalid book_id")
        return

    book_name, book_name_id = book
    issued_date = date.today()
    renew_date = issued_date + timedelta(days=15)

    try:
        cursor.execute(
            "UPDATE all_books SET is_issued=1 WHERE book_id=?",
            (book_id,)
        )
        cursor.execute(
            "INSERT INTO published_books VALUES(?,?,?,?,?,?)",
            (
                enrollment_no,
                book_id,
                book_name_id,
                book_name,
                issued_date,
                renew_date
            )
        )
        connect.commit()
        print("Book issued successfully")

    except:
        connect.rollback()
        print("Transaction failed")
# ------------------ FUNCTIONS ------------------







# ------------------ MAIN ------------------
def main():

    enrollment_no = input("Enter your enrollment number: ")
    show_student_details(enrollment_no)

    print("\n1. Publish Book")
    print("2. Renew Book")
    print("3. Submit Book")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        issue_book(enrollment_no)
    elif choice == 2:
        pass
    elif choice == 3:
        pass

    connect.close()

if __name__ == "__main__":
    main()
# ------------------ MAIN ------------------
