# Library Management System

import json
from datetime import date


# Loading data from JSON files
def load_data(file_name):
    try:
        file = open(file_name, "r")
        data = json.load(file)
        file.close()
        return data
    except FileNotFoundError:
        return []


# Saving data in JSON files
def save_data(file_name, data):
    file = open(file_name, "w")
    json.dump(data, file, indent=4)
    file.close()


books = load_data("books.json")
students = load_data("students.json")
issued_books = load_data("issued_books.json")


# 1. Add New Book
def add_book():
    book_id = input("Enter book ID: ")

    for book in books:
        if book["book_id"].lower() == book_id.lower():
            print("Book ID already exists!")
            return

    book_name = input("Enter book name: ")
    author = input("Enter author name: ")
    category = input("Enter category: ")

    try:
        copies = int(input("Enter number of copies: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if copies <= 0:
        print("Number of copies must be greater than zero.")
        return

    book = {
        "book_id": book_id,
        "book_name": book_name,
        "author": author,
        "category": category,
        "available_copies": copies
    }

    books.append(book)
    save_data("books.json", books)
    print("Book added successfully!")


# 2. Display All Books
def display_books():
    if not books:
        print("No books available.")
        return

    for book in books:
        print("\n------------------------------")
        print("Book ID:", book["book_id"])
        print("Book Name:", book["book_name"])
        print("Author:", book["author"])
        print("Category:", book["category"])
        print("Available Copies:", book["available_copies"])


# 3. Search for a Book
def search_book():
    search = input("Enter Book ID, Book Name or Author Name: ").lower()
    found = False

    for book in books:
        if (search == book["book_id"].lower() or
                search in book["book_name"].lower() or
                search in book["author"].lower()):

            print("\nBook Found!")
            print("Book ID:", book["book_id"])
            print("Book Name:", book["book_name"])
            print("Author:", book["author"])
            print("Category:", book["category"])
            print("Available Copies:", book["available_copies"])
            found = True

    if found == False:
        print("Book not found!")


# 4. Register a Student
def register_student():
    student_id = input("Enter student ID: ")

    for student in students:
        if student["student_id"].lower() == student_id.lower():
            print("Student ID already exists!")
            return

    name = input("Enter student name: ")
    department = input("Enter department: ")
    contact = input("Enter contact number: ")

    student = {
        "student_id": student_id,
        "name": name,
        "department": department,
        "contact": contact
    }

    students.append(student)
    save_data("students.json", students)
    print("Student registered successfully!")


# 5. Issue a Book
def issue_book():
    student_id = input("Enter student ID: ")
    book_id = input("Enter book ID: ")

    student_found = False
    book_found = False

    for student in students:
        if student["student_id"].lower() == student_id.lower():
            student_found = True
            break

    for book in books:
        if book["book_id"].lower() == book_id.lower():
            book_found = True
            selected_book = book
            break

    if student_found == False:
        print("Student not registered!")
        return

    if book_found == False:
        print("Book not found!")
        return

    if selected_book["available_copies"] <= 0:
        print("No copies available!")
        return

    selected_book["available_copies"] = selected_book["available_copies"] - 1

    record = {
        "student_id": student_id,
        "book_id": selected_book["book_id"],
        "issue_date": str(date.today())
    }

    issued_books.append(record)

    save_data("books.json", books)
    save_data("issued_books.json", issued_books)
    print("Book issued successfully!")


# 6. Return a Book
def return_book():
    student_id = input("Enter student ID: ")
    book_id = input("Enter book ID: ")

    for record in issued_books:
        if (record["student_id"].lower() == student_id.lower() and
                record["book_id"].lower() == book_id.lower()):

            for book in books:
                if book["book_id"].lower() == book_id.lower():
                    book["available_copies"] = book["available_copies"] + 1
                    break

            issued_books.remove(record)

            save_data("books.json", books)
            save_data("issued_books.json", issued_books)
            print("Book returned successfully!")
            return

    print("Issue record not found!")


# 7. Display Issued Books
def display_issued_books():
    if not issued_books:
        print("No books are currently issued.")
        return

    for record in issued_books:
        print("\n------------------------------")
        print("Student ID:", record["student_id"])
        print("Book ID:", record["book_id"])
        print("Issue Date:", record["issue_date"])


# 8. Delete a Book
def delete_book():
    book_id = input("Enter book ID to delete: ")

    for record in issued_books:
        if record["book_id"].lower() == book_id.lower():
            print("This book is currently issued. Cannot delete it!")
            return

    for book in books:
        if book["book_id"].lower() == book_id.lower():
            books.remove(book)
            save_data("books.json", books)
            print("Book deleted successfully!")
            return

    print("Book not found!")


# 9. Main Function
def main():
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add New Book")
        print("2. Display All Books")
        print("3. Search for a Book")
        print("4. Register a Student")
        print("5. Issue a Book")
        print("6. Return a Book")
        print("7. Display Issued Books")
        print("8. Delete a Book")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            register_student()
        elif choice == "5":
            issue_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            display_issued_books()
        elif choice == "8":
            delete_book()
        elif choice == "9":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()
