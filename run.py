import datetime
import gspread

from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('SchoolDatabase')
STUDENTS = SHEET.worksheet("studentdata")


def main():
    """
    Function to display main menu
    """
    while True:
        print("")
        print("What would you like to do?")
        print("""
                    --------MENU--------
                    1. Add new student\n\
                    2. Search for student\n\
                    3. Display all students\n\
                    4. Delete student\n\
                    5. Reset database\n\
                    6. Exit\n
                        """)
        user_input = input("Please from 1 - 6: ")
        if user_input == "1":
            add_new_student()
        elif user_input == "2":
            search_for_student()
        elif user_input == "3":
            display_all_students()
        elif user_input == "4":
            delete_student()
        elif user_input == "5":
            remove_all_students()
        elif user_input == "6":
            exit_program()
        else:
            print("Invalid choice")
            print("Please enter a number from 1-6.")
            pass


def add_new_student():
    """
    Function to add new student by name, age
    test results, and course dates
    """
    student_details = []
    # function for adding student's surname
    while True:
        family_name = input("Please enter the student's family name: ")

        if validate_data(family_name):
            student_details.append(family_name)
            break
    # function for adding student's first name
    while True:
        first_name = input("Please enter the student's first name: ")

        if validate_data(first_name):
            student_details.append(first_name)
            break
    # function for adding student's nationality
    while True:
        nationality = input("Please enter the student's nationality: ")
        if validate_data(nationality):
            student_details.append(nationality)
            break
    # function for adding student's age
    while True:
        age = input("Please enter the student's age: ")
        if validate_numeric_data(age):
            student_details.append(int(age))
            break
    # function for adding student's test results
    while True:
        test_results = input("Please enter the student's"
                             " test results (1-30): ")
        if validate_numeric_data(test_results) and \
           int(test_results) <= 30 and int(test_results) > 0:
            student_details.append(int(test_results))
            break
        else:
            pass
    # function for adding a level to student's test results
    while True:
        if int(test_results) >= 1 and int(test_results) <= 5:
            student_level = "A1"
        elif int(test_results) >= 6 and int(test_results) <= 10:
            student_level = "A2"
        elif int(test_results) >= 11 and int(test_results) <= 15:
            student_level = "B1"
        elif int(test_results) >= 16 and int(test_results) <= 23:
            student_level = "B2"
        elif int(test_results) >= 23 and int(test_results) <= 28:
            student_level = "C1"
        elif int(test_results) >= 29 and int(test_results) <= 30:
            student_level = "C2"

        student_details.append(student_level)
        break

    # function for adding student's start and end dates
    while True:
        try:
            start_date = input("Please enter the start date"
                                "(use only DD-MM-YYYY): ")
            end_date = input("Please enter the end date "
                             "(use only DD-MM-YYYY): ")

            if validate_date(start_date, end_date):
                student_details.append(start_date)
                student_details.append(end_date)
                break
                display_message("The start date is later than the end date."
                                "  Please enter the dates again.")

        except Exception:
            pass

    # generates student number
    studentIds = STUDENTS.col_values(9)[1:]
    results = [int(i) for i in studentIds]
    maxId = max(results)
    student_id = int(maxId) + 1
    student_details.append(student_id)

    # function for confirming student to be added
    while True:
        headings = STUDENTS.row_values(1)
        summary = dict(zip(headings, student_details))
        print("------")
        for x, y in summary.items():
            print(x, ": ", y)
        print("------")

        confirmation = input("Please confirm that you wish to"
                             " add this student to the database? (Y/N) ")

        if confirmation.upper() == "Y":
            display_message("Accessing database..........")
            display_message("Updating database..........")
            SHEET.worksheet('studentdata').append_row(student_details)
            STUDENTS.sort((1, 'asc'))
            display_message("Student added succesfully!")
            add_another_student()

        elif confirmation.upper() == "N":
            next_step = input("Do you want to add another new student? (Y/N) ")
            if next_step.upper() == "Y":
                display_message("Restarting add new student")
                add_new_student()
            elif next_step.upper() == "N":
                display_message("Returning to main menu")
                main()
        else:
            print("Please enter 'Y' or 'N'")


def add_another_student():
    """
    Function give user the option of adding another student without
    exiting to the main menu
    """
    while True:
        next_step = input("Do you want to add another new student? (Y/N) ")
        if next_step.upper() == "Y":
            display_message("Restarting add new student")
            add_new_student()
        elif next_step.upper() == "N":
            display_message("Returning to main menu")
            main()
        else:
            print("Please enter 'Y' or 'N'")


def validate_data(values):
    """
    Function to validate that the input data is letters
    """
    try:
        if values.isalpha() is False:
            raise ValueError()
    except ValueError as e:
        display_message("Please make sure you only use letters."
                        "  \nSpecial characters and numbers are not allowed")
        return False

    return True


def validate_numeric_data(values):
    """
    Function to validate that the input data is numeric
    """
    try:
        if values.isnumeric() is False:
            raise ValueError()
        elif values == "0":
            raise ValueError()
    except ValueError as e:
        display_message("Please enter a number greater than 0."
                        "  \nSpecial characters and letters are not allowed.")
        return False

    return True


def validate_date(start_date, end_date):
    """
    Function to validate the date format as DD-MM-YYYY
    """
    try:
        if datetime.datetime.strptime(start_date, '%d-%m-%Y') is False:
            raise ValueError()
        elif datetime.datetime.strptime(end_date, '%d-%m-%Y') is False:
            raise ValueError()
        try: 
            if start_date > end_date:
                raise ValueError()
        except ValueError as e:
            display_message("Your start date is later than your end date. "
                            "\nPlease enter the dates again.")
            return False

    except ValueError as e:
        display_message("Please enter the date as DD-MM-YYYY."
                        " \nOther date formats will not be accepted"
                        " by the program.")

        return False

    return True


def display_all_students():
    """
    Function to add all students to a list
    """
    wks = STUDENTS.get_all_records()
    if wks:
        for student in wks:
            print_all_students(student)
    else:
        print("None")


def print_all_students(existing):
    """
    Function to display all students in a list
    """
    student = []
    print("---")
    for key, value in existing.items():
        print(f'{key}: {value}')
    print("---")
    return student
    main()


def search_for_student():
    """
    Function to search by student's ID number
    """
    while True:
        number = input("Please enter the Student ID number"
                       " \n(or input 0 to return to the main menu): ")
        student = STUDENTS.col_values(9)
        if number in student:
            rownum = student.index(number) + 1
            row = STUDENTS.row_values(rownum)
            headings = STUDENTS.row_values(1)
            search_results = dict(zip(headings, row))
            print("")
            for x, y in search_results.items():
                print(x, ": ", y)
            print("------")
        elif number == "0":
            main()
        else:
            display_message("There is currently no student with that number."
                            "  Please enter a valid student number.\n"
                            " Please type '0' to return to the main menu.")
            pass

        search_again = input("Would you like to search for"
                             " another student? (Y/N) ")
        if search_again.upper() == "Y":
            display_message("Restarting Student Search")
            search_for_student()
        elif search_again.upper() == "N":
            display_message("Returning to main menu")
            main()


def delete_student():
    """
    function to delete a single student from the spreadsheet
    """
    while True:
        try:
            number = input("Please enter the Student ID number.\n"
                           "Enter '0' to return to the main menu. ")
            student = STUDENTS.col_values(9)
            if number in student:
                rownum = student.index(number) + 1
                row = STUDENTS.row_values(rownum)
                headings = STUDENTS.row_values(1)
                search_results = dict(zip(headings, row))
                print("")
                for x, y in search_results.items():
                    print(x, ": ", y)
                print("------")
                confirm_student_removal()
                STUDENTS.delete_rows(rownum)
            elif number.isalpha():
                display_message("Invalid input.  Please enter a valid student"
                                " number. \nEnter '0' to return to the"
                                " main menu. ")
            elif int(number) == 0:
                display_message("Returning to main menu.")
                main()
            else:
                display_message("Invalid input - there is no student"
                                " with that number."
                                " Please enter a valid student number."
                                "\nEnter '0' to return to the main menu. ")

        except Exception():
            pass


def confirm_student_removal():
    """
    Function to confirm the removal of student to ensure
    the user has not made a mistake
    """
    confirmation = input("Are you sure you want to delete this student?"
                         " (Y/N)\nThis action cannot be undone. ")
    if confirmation.upper() == "Y":
        display_message("Removing student from database")
        display_message("Student has been removed from database")
        next_step = input("Do you wish to remove another student? (Y/N) ")
        if next_step.upper() == "Y":
            delete_student()
        elif next_step.upper() == "N":
            display_message("Returning to main menu")
            main()
    elif confirmation.upper() == "N":
        display_message("Returning to main menu")
        main()
    else:
        display_message("Invalid Input.  Please choose Y or N")
        confirm_student_removal()


def exit_program():
    """
    Function to exit the program
    """
    print("""
                THANK YOU FOR USING THIS PROGRAM
                        HAVE A NICE DAY

                        """)
    exit()


def remove_all_students():
    """
    Function to clear database of all students
    """
    while True:
        confirmation = input("Are you sure you want to clear the database?"
                             "\nThis action cannot be undone. (Y/N) ")
        if confirmation.upper() == "Y":
            STUDENTS.clear()
            headings = ("Family Name", "First Name", "Nationality", "Age",
                        "Test Results", "Level", "Start Date",
                        "End Date", "Student Number")
            STUDENTS.append_row(headings)
            display_message("Accessing database")
            display_message("Removing students from database")
            display_message("All students have been removed from the database")
            display_message("Returning to main menu")
            main()
        elif confirmation.upper() == "N":
            display_message("Returning to main menu")
            main()
        else:
            display_message("Invalid Input.  Please choose Y or N")


def display_message(message):
    print("")
    print("----------")
    print("")
    print(message)
    print("")
    print("----------")
    print("")

main()
