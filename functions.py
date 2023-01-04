#Look at app.py in book_database_project to see how to clean the CSV data & load it into the db
from models import *

import datetime
import csv
from datetime import date

def clean_price(input_price):
    try:
        price_split = input_price.split('$')
        price_float = float(price_split[1])
    except ValueError:
        input('''
        \n**** Price Error ****
        \rThe date format should only include: dollars & cents separated with a period
        \rEx: 24.56
        \rPress Enter to try again
        \r********************''')
        return
    else:
        return int(price_float * 100)  

def clean_date(date_str):
    try:
        month = int(date_str.split('/')[0])
        day = int(date_str.split('/')[1])
        year = int(date_str.split('/')[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n**** Date Error ****
        \rThe date format should be: MONTH DD, YYYY & in the past
        \rEx: March 22, 1965
        \rPress Enter to try again
        \r********************''')
        return
    else: 
        return return_date

def clean_quantity(given_quantity):
    try:
        cleaned_quantity = int(given_quantity)
    except ValueError:
        input('''
        \n**** Quantity Error ****
        \rThe quantity must be a whole number (Can't be fractions, decimals, or letters)
        \rEx: 10, 456, etc...
        \rPress Enter to enter a new quantity
        \r********************
        ''')
        return
    else:
        return cleaned_quantity


def add_csv(input_file):
    with open(input_file) as csvfile:
        if input_file == 'csv/inventory.csv':
            data = csv.reader(csvfile)
            next(data) #skips header row
            for row in data:
                inventory_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
                if inventory_in_db == None:
                    product_name = row[0]
                    product_price = clean_price(row[1])
                    product_quantity = int(row[2])
                    date_updated = clean_date(row[3])
                    query = session.query(Brands).filter(Brands.brand_name == row[4]).all()
                    for info in query:
                        brand_id = info.brand_id
                    new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
            session.commit()
        elif input_file == 'csv/brands.csv':
            data = csv.reader(csvfile)
            next(data) #skips header row
            for row in data:
                brand_in_db = session.query(Brands).filter(Brands.brand_name==row[0]).one_or_none()
                if brand_in_db == None:
                    brand_name = row[0]
                    new_brand = Brands(brand_name=brand_name)
                    session.add(new_brand)
            session.commit()

# main menu - V: details of a single product - N: add a new product - A: view an analysis - B: make a backup
def menu():
    while True:
        print('''
            \nStore Inventory Menu\n
            \rV. See details of a product
            \rN. Add a new product
            \rA. See an analysis of all products
            \rB. Backup the database as a CSV file
            \rE. Exit
            ''')
        choice = input('What would you like to do? ')
        if choice in ['V', 'N', 'A', 'B', 'E']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above
            \rPress enter to choose again
            ''')

def view_product():
    current_product_ids = []
    for product_id_number in session.query(Product.product_id):
        current_product_ids.append(product_id_number[0])
    try:
        product_searched = int(input('\nPlease enter the product ID number: '))
        if product_searched in current_product_ids:
            result = (session.query(Product).filter(Product.product_id == product_searched).all())[0]
            product_brand = session.query(Brands.brand_name).filter(Brands.brand_id == result.brand_id).all()[0].brand_name
            print(f'''
                \nProduct details
                \r***************\n
                \rProduct name: {result.product_name}
                \rProduct price: ${result.product_price/100}
                \rNumber in stock: {result.product_quantity}
                \rDate updated: {result.date_updated}
                \rBrand of product: {product_brand}
            ''')
        else:
            raise Exception
    except Exception:
        input('\nSelected product ID does not exist. \nPress enter to try another product ID')
        view_product()

def get_brand_id_from_brand_name():
    current_brand_names = []
    for products in session.query(Brands.brand_name):
        current_brand_names.append(products[0])
    print('\nCurrent brands:')
    index_list = []
    for index, brand in enumerate(current_brand_names, 1):
        print(f'{index}. {brand}')
        index_list.append(index)
    try:
        user_choice = int(input('\nSelect the brand by entering the corresponding number from the above list: '))
        if user_choice not in index_list:
            raise Exception
    except:
        input('''
        \n**** Brand Error ****
        \rThe entered value must be a number from the give list
        \rPress enter to prick the brand again
        \r**********************
        ''')
        return
    else:
        return user_choice

def add_product():
    print('''
    \nAdd new product
    \r***************\n''')
    product_name = input('Enter product name: ')
    quantity_error = True
    while quantity_error:
        product_quantity = clean_quantity(input('Enter the quantity of the product: '))
        if type(product_quantity) == int:
            quantity_error = False
    price_error = True
    while price_error:
        product_price = clean_price('$'+input('Enter the price in dollars & cents (ex. 25.28): '))
        if type(product_price) == int:
            price_error = False
    date_updated = today = date.today()
    brand_id_error = True
    while brand_id_error:
        brand_id = get_brand_id_from_brand_name()
        if type(brand_id) == int:
            brand_id_error = False
    print(product_name, product_price, product_quantity, date_updated, brand_id)
    print(type(product_name), type(product_price), type(product_quantity), type(date_updated), type(brand_id))
    # new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
    # session.add(new_product)
    # session.commit()

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            view_product()
            #Todo: Set input to uppercase 
            input('\nPress any key to return to the main menu ')
            app()
        elif choice == 'N':
            add_product()
            #Todo: Set input to uppercase 
            input('\nProduct added. \rPress any key to return to the main menu ')
            app()
        elif choice == 'E':
            app_running = False
    exit("\nSee you next time! \U0001f44b\n")


app()