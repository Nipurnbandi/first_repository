import sqlite3
import os
from datetime import date, timedelta, datetime

# ------------------ DB CONNECTION ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Library.db")

connect = sqlite3.connect(db_path)   
cursor = connect.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
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
def insert_sample_data():
    cursor.execute("DELETE FROM published_books")
    cursor.execute("DELETE FROM all_books")
    cursor.execute("DELETE FROM quantity_books")
    cursor.execute("DELETE FROM student")

    cursor.executemany(
        "INSERT INTO student VALUES(?,?)",
        [
            ('0176AL241084','Nipurn Bandi'),
            ('0176AL241085','Sankalp Sharma'),
            ('0176AL241086','OM Kumar'),
            ('0176AL241087','OM Gupta'),
            ('0176AL241088','Anand Bhaghel')
        ]
    )

    cursor.executemany(
        "INSERT INTO quantity_books VALUES(?,?,?,?)",
        [
            ('B001','Python Programming','Computer Science',3),
            ('B002','Data Structures','Computer Science',2),
            ('B003','Database Systems','Computer Science',2),
            ('B004','Operating Systems','Computer Science',2),
            ('B005','Computer Networks','Computer Science',1),
            ('B006','Artificial Intelligence','AI',2),
            ('B007','Machine Learning','AI',1)
        ]
    )

    cursor.executemany(
        "INSERT INTO all_books VALUES(?,?,?,0)",
        [
            ('PY001','B001','Python Programming'),
            ('PY002','B001','Python Programming'),
            ('PY003','B001','Python Programming'),
            ('DS001','B002','Data Structures'),
            ('DS002','B002','Data Structures'),
            ('DB001','B003','Database Systems'),
            ('DB002','B003','Database Systems'),
            ('OS001','B004','Operating Systems'),
            ('OS002','B004','Operating Systems'),
            ('CN001','B005','Computer Networks'),
            ('AI001','B006','Artificial Intelligence'),
            ('AI002','B006','Artificial Intelligence'),
            ('ML001','B007','Machine Learning')
        ]
    )

    connect.commit()




def calc_renew(enrollment_no):
    cursor.execute(
        "SELECT renew_date FROM published_books WHERE enrollment_no=?",
        (enrollment_no,)
    )

    fine = 0
    for (renew_date,) in cursor.fetchall():
        renew_date = datetime.strptime(renew_date, "%Y-%m-%d").date()
        overdue = (date.today() - renew_date).days
        if overdue > 0:
            fine += overdue * 10
    return fine
        



def no_of_book_issued(enrollment_no):
    cursor.execute("SELECT COUNT(*) FROM published_books WHERE enrollment_no=?",(enrollment_no,))
    data=cursor.fetchone()[0]
    return data
       



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
        "SELECT book_name,issued_date,renew_date FROM published_books WHERE enrollment_no=?",
        (enrollment_no,)
    )

    
    for book_name,issued_date,renew_date in cursor.fetchall():
        print(book_name,issued_date,renew_date)

    
def renew_book(book_id,enrollment_no ):
    cursor.execute(
        "SELECT book_name,issued_date,renew_date FROM published_books WHERE book_id=?",
        (book_id,)
    )
    data=cursor.fetchone()
    if data is None:
        print("Wrong book id")
        return


    new_date=str(date.today()+timedelta(days=15))
    cursor.execute('''UPDATE published_books
                    SET renew_date=? 
                    WHERE book_id=?''',(new_date,book_id))
    connect.commit()
    print("published suecessfully")






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



def submit_book(book_id,enrollment_no):
    cursor.execute("SELECT * FROM published_books WHERE book_id=?",(book_id,))
    data=cursor.fetchone()
    if data is None:
        print("book id wrong or book wasnt issued from library")
        return
    
    cursor.execute("DELETE FROM published_books WHERE book_id=?",(book_id,))
    connect.commit()
    cursor.execute('''UPDATE all_books
                  SET is_issued=0
                  WHERE book_id=?''',(book_id,))
    connect.commit()
    print("Book submited successfully")

    cursor.execute(
        "SELECT book_name,issued_date,renew_date FROM published_books WHERE enrollment_no=?",
        (enrollment_no,)
    )

    
    for book_name,issued_date,renew_date in cursor.fetchall():
        print(book_name,issued_date,renew_date)
    

# ------------------ FUNCTIONS ------------------







# ------------------ MAIN ------------------
def main():
    
    
    
    enrollment_no = input("Enter your enrollment number: ")
    cursor.execute("SELECT * FROM student WHERE enrollment_no=?",(enrollment_no,))
    data=cursor.fetchone()
    if data is None:
        print("No such roll number exist")
        return


    show_student_details(enrollment_no)
    fine=calc_renew(enrollment_no)
    print("\nOverdue:",fine)

    if fine>0:
        print("First pay overdue")
        response=input("Paid or not (y/n)")
        if response=="y":
            print()
        elif response=="n":
            return
        else:
            print("Wrong response entered")
            return






    print("\n1. Publish Book")
    print("2. Renew Book")
    print("3. Submit Book")

    choice = int(input("Enter your choice: "))

    if choice == 1:

        books_issued=no_of_book_issued(enrollment_no)
        if books_issued==4:
            print("Reached limit to publish books,already 2 books issued")
            return
        
        issue_book(enrollment_no)
    elif choice == 2:
        book_id=input("Enter book ID:")
        renew_book(book_id,enrollment_no)
    elif choice == 3:
        book_id=input("Enter book ID:")
        submit_book(book_id,enrollment_no)
        



if __name__ == "__main__":
    main()
# ------------------ MAIN ------------------
