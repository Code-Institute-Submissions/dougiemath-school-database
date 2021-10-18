import gspread
from email.utils import parseaddr
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
STUDENT_DATA = SHEET.worksheet("studentdata")

def add_new_student():
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

    print(student_details)

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

add_new_student()

