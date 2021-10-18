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

student_data = SHEET.worksheet('studentdata')
data = student_data.get_all_values()

def start():
    """
    Adds a contents menu for users to navigate
    """
    print("""
                --------MENU--------
                1. Add new student
                2. Search student
                3. Check Level
                4. Show all students
                5. Exit
                    """)
    while True:
        selection = input("Pick a number: \n")
        if selection == '1':
            add_student()
            break
        elif selection == '2':
            search_student()
            break
        elif selection == '3':
            display_all_students()
            break
        elif selection == '4':
            check_level()
            break
        elif selection == '5':
            exit()
            break
        else:
            print("Invalid choice, please enter a number 1-3")

def add_student():
    print("this is the add student")


def search_student():
    print("this is the search student")

def display_all_students():
    print("This displays everyone")

def check_level():
    print("This checks level")

def exit():
    print("this is the end")

def main():
    start()

main()

