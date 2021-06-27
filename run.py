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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

def get_sales_data():
    """
    Get sales inputs from the user
    """
    print("Please enter sales data from the last market")
    print("Data should be six numbers seperated by commas")
    print("Example: 10,14,23,32,31,25 \n")

    data_str = input("Enter your data here:")
    sales_data = data_str.split(",")
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try convert all values into integers
    Raise ValueError if strings cannot be converted into int,
    or there aren't exactly six values
    """

    try:
        if len(values) != 6:
            [int(value) for value in values]
            raise ValueError(
                f"Exactly six values required, you entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")


get_sales_data()
