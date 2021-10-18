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
STUDENT_DATA = SHEET.worksheet("studentdata")

def add_new_student():
    family_name = input("Please enter the student's family name: ")
    validate_data(family_name)

def validate_data(values):
    print(values)
    try:
        if values.isalpha() == False:
            raise ValueError(
                    "Try again"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")



add_new_student()