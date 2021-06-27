import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers seperated by commas")
        print("Example: 10,14,23,32,31,25 \n")

        data_str = input("Enter your data here:")
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data entered is valid")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try convert all values into integers
    Raise ValueError if strings cannot be converted into int,
    or there aren't exactly six values
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:         
            raise ValueError(
                f"Exactly six values required, you entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    update sales worksheet with new row of data
    """

    print("Updating sales worksheet")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each item
    Positive surplus indicates waste and negative surplus indicates 
    extra made when stock was sold out
    """
    print("Calculating surplus data")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock,sales in zip(stock_row,sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def main():
    """
    Call all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("Welcome to Love Sandwhich Automation")
main()