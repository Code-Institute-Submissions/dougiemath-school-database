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


def add_new_student():
    """
    Function to add new student by name, age
    test results, and course dates
    """
    student_details = []
    while True:
        family_name = input("Please enter the student's family name: ")
        validate_data(family_name)
       
        if validate_data(family_name):
            student_details.append(family_name)
            break

    while True:
        first_name = input("Please enter the student's first name: ")
        validate_data(first_name)
       
        if validate_data(first_name):
            student_details.append(first_name)
            break
    
    while True:
        nationality = input("Please enter the student's nationality: ")
        validate_data(nationality)
       
        if validate_data(nationality):
            student_details.append(nationality)
            break

    while True:
        age = input("Please enter the student's age: ")
        validate_numeric_data(age)
       
        if validate_numeric_data(age):
            student_details.append(int(age))
            break

    while True:
        test_results = input("Please enter the student's test results: ")
        validate_numeric_data(test_results)
       
        if validate_numeric_data(test_results):
            student_details.append(int(test_results))
            break
    
    while True:
        try:
            start_date = input("Please enter the start date: ")
            validate_date(start_date)
            end_date = input("Please enter the end date: ")
            validate_date(end_date) 
        
            if validate_date(start_date) and validate_date(end_date) and end_date > start_date:
                student_details.append(start_date)
                student_details.append(end_date)
                break
            else:
               print("Nope")
               
        except Exception:
            pass

    #add data to google sheet
    SHEET.worksheet('studentdata').append_row(student_details)
    


"""
Functions for validating user input in
add_new_student()
"""

def validate_data(values):
    try:
        if values.isalpha() == False:
            raise ValueError(
                    "please make sure you only use letters.  Special characters are not allowed "
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
   
    return True

def validate_numeric_data(values):
    try:
        if values.isnumeric() == False:
            raise ValueError(
                    "please make sure you only use numbers."
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def validate_date(values):
    try:
        if datetime.datetime.strptime(values, '%d-%m-%Y') == False:
            raise ValueError(
                    "please make sure you only use numbers."
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

add_new_student()

