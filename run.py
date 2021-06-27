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

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the relevant data provided
    """
    print(f"Updating workshee {worksheet}...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} updated successfully\n")

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

def get_last_5_entries_sales():
    """
    Collect last 5 entries for each sandwich from sales worksheet and return
    the data as a list of lists
    """
    sales = SHEET.worksheet('sales')
    #column = sales.col_values(3)
    #print(column)

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item,  adding 10%
    """
    print("Calculating stock data\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    """
    Call all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,'stock')

print("Welcome to Love Sandwhich Automation")

main()
