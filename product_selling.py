# Laptop Selling Website
# Date: 
# Subject: FCSP-1
# Prepared By:
# Aakash Kishanbhai Prajapati - 23002170120001
# Maniar Om Vimalbhai - 23002171220008 
# Mahir


# FOR PDF GENERATION:
# pip install reportlab

# FOR MYSQL CONNECTION:
# pip install mysql-connector-python

import mysql.connector
from reportlab.pdfgen import canvas

db_host="localhost"
db_user="root"
db_pswd="abcd"
db_port="3307"
conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pswd, database="product_db", port=db_port)

#------------------------------------------------------------------------#
# Product Class                                                          #
#------------------------------------------------------------------------#

class Product:
    """
    A class represting product related operation
    """
    def __init__(self):
        """
        Initialitzes Product Object for initiating product related operations.
        Asks to select two of the available categories
        """
        print("\n---------------------------------------------------")
        print("CATEGORIES:")
        print("\n---------------------------------------------------\n")
        print("1. Gaming Laptops")
        print("2. Work Laptops")
        print("3. Go back to main menu")
        try:
            category = int(input("\nEnter the category of the laptop you want to buy: "))
            print("\n---------------------------------------------------")
            if category == 1:
                buy_laptop("Gaming")
            elif category == 2:
                buy_laptop("Work")
            elif category == 3:
                main()
            else:
                print("Invalid Input")
                product = Product()
        except ValueError:
            print("Invalid Input")
            product = Product()


class Cart:
    """
    A class containing cart related methods.
    """
    def __init__(self):
        """
        Initialitzes Product Object for initiating product related operations.
        It gives four options to select from.
        """
        print("\n---------------------------------------------------")
        print("CART MENU")
        print("---------------------------------------------------\n")
        print("1. View Cart")
        print("2. Remove item")
        print("3. Checkout")
        print("4. Return To Main Menu")
        try:
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                self.show_cart()
        
            elif choice == 2:
                self.remove_item()
            
            elif choice == 3:
                self.checkout()

            elif choice == 4:
                main()
            else:
                print("Invalid Input")
                cart = Cart()
        except ValueError:
            print("Invalid Input")
            cart = Cart()

    def show_cart(self):
        """
        This method displays items available in the cart from the database.
        """
        print("\n---------------------------------------------------")
        print("CART")
        print("---------------------------------------------------\n")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_db.cart")
        items = cursor.fetchall()
        if items:
            for index,value in enumerate(items):
                print(index+1,":",value[1],", Category: ",value[2],", Price: Rs.",value[3], ". Quantity: ",value[4])
        else:
            print("No Laptops Added in Cart")
            print("\n---------------------------------------------------")
        
        cart = Cart()


    def remove_item(self):
        """
        This method removes an item from the cart.
        """
        print("\n---------------------------------------------------")
        print("CART")
        print("---------------------------------------------------\n")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_db.cart")
        items = cursor.fetchall()
        if items:
            for index,value in enumerate(items):
                print(index+1,":",value[1],", Category: ",value[2],", Price: Rs.",value[3], ", Quantity: ",value[4])
            choice = validate_index(len(list(enumerate(items))))
            
            print("\n---------------------------------------------------")
            print("\nThe chosen laptop is:")
            for index,value in enumerate(items):
                if index+1 == choice:
                    print(value[1],", Category: ",value[2],", Price: Rs.",value[3], ", Quantity: ",value[4])
                    chosen_laptop = value
            print("\n---------------------------------------------------")
            
            confirm = validate_confiramtion()
            if confirm:
                cursor.execute("DELETE FROM `product_db`.`cart` WHERE (`cid` = '%s')",[chosen_laptop[0]])
                cursor.execute("SELECT * FROM product_db.product WHERE (`name` = %s)",[chosen_laptop[1]])
                product = cursor.fetchone()
                cursor.execute("update product_db.product set stock = stock +  %s where pid = '%s'",(chosen_laptop[4],product[0]))
                conn.commit()
                print("\nLaptop removed from Cart")
                cart = Cart()
            else:
                cart = Cart()

        else:
            print("No Laptops Added in Cart")
            print("\n---------------------------------------------------")
        
        cart = Cart()
    
    def checkout(self):
        """
        This method takes all the items from cart and generates bill if cart contains products
        """
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_db.cart")
        items = cursor.fetchall()
        if items:
            # initialized variables
            line = 0
            total_price = 0
            # creating pdf file
            pdf = canvas.Canvas('Order.pdf')
            # setting font
            pdf.setFont('Helvetica-Bold', 24)
            pdf.drawString(250, 730, "Your Order")
            pdf.setFont('Helvetica', 16)
            pdf.drawString(100, 670, "Product")
            pdf.drawString(240, 670, "Type")
            pdf.drawString(310, 670, "Unit Price")
            pdf.drawString(400, 670, "Quantity")
            pdf.drawString(475, 670, "Total")

            pdf.setFont('Helvetica', 12)

            # row[0]: id
            # row[1]: name
            # row[2]: category
            # row[3]: per unit price
            # row[4]: quantity
            # row[5]: total_price
            for row in items:
                pdf.drawString(50, 640-(30*line), f"{line+1}.")
                pdf.drawString(100, 640-(30*line), str(row[1]))
                pdf.drawString(240, 640-(30*line), str(row[2]))
                pdf.drawString(325, 640-(30*line), str(row[3]))
                pdf.drawString(420, 640-(30*line), str(row[4]))
                pdf.drawString(475, 640-(30*line), str(row[5]))
                total_price += row[5]
                pdf.line(50, 630-(30*line), 525, 630-(30*line))
                line += 1
            
            pdf.drawString(370, 630-(30*line), f"Total Amount: Rs.{total_price}")
            try:
                pdf.save()
                print("PDF file saved.\n")
            except PermissionError:
                print("Permission Denied. Please close the file")
                main()
        else:
            print("No Laptops Added in Cart")
            print("\n---------------------------------------------------")
            main()


def validate_index(rows):
    """
    Takes input from the user from the list and validates for correct row.

    Parameters:
        rows (list): Consist of list of laptops available.

    Returns:
        row_index (int): index of the selected laptop.
    """
    try:
        row_index = int(input("\nEnter the index number of laptop from list: "))
        if row_index > 0 and row_index <= rows:
            return row_index
        else:
            print("Invalid Input")
            return validate_index(rows)
    except ValueError:
        print("Invalid Input")
        return validate_index(rows)
    
def validate_confiramtion():
    """
    Takes a yes or no input from user and validates thier confirmation.

    Returns: 
        True: When user agrees.
        False: When user denies.
        validate_confiramtion(): when user enters any other string than y or n.
    """
    confirm = input("\nAre you sure? (y/n): ")
    if confirm == "y" or confirm == "Y":
        return True
    elif confirm == "n" or confirm == "N":
        return False
    else:
        print("Invalid Input")
        return validate_confiramtion()
    
def validate_quantity(inventory):
    """
    It asks for input of quantity of laptop and checks that wheter the amount entered is valid or not. 
    The amount will only be valid when entered amount is more than 0 and less than the inventory.

    Parameters:
        inventory (int): 

    Returns:
        Quantity (int): Quantity that user has entered
        validate_quantity(inventory): when user fails to enter correct amount
    """
    print("\n---------------------------------------------------")
    print("\nAvailable Stock =",inventory)
    try:
        quantity = int(input(f"\nEnter the quantity of laptop you want to purchase: "))
        if quantity > 0 and quantity <= inventory:
            return quantity
        else:
            print(f"\nEnter More than 0 and less than or equal to {inventory} for buying laptop.")
            return validate_quantity(inventory)
    except ValueError:
        print(f"\nEnter More than 0 and less than or equal to {inventory} for buying laptop.")
        return validate_quantity(inventory)   

def buy_laptop(category):
    """
    Used to buy laptop. It displays all the laptops based on given category and asks user to select one laptop from list.
    After getting which laptop user wants to buy, it calls all validation related methods and if all validations are fullfilled it will than insert the data in cart table of databse.

    Parameters:
        category (str): The category of laptop which needs to be displayed
    """
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM product_db.product WHERE category = %s AND stock > 0",[category])
    rows = cursor.fetchall()
    if rows:
        print("Available Laptops")
        print("---------------------------------------------------\n")
        # 0: id, 1: name, 2: category, 3:price, 4: stock
        for index,value in enumerate(rows):
            print(index+1,":",value[1],", Price:  Rs.",value[3],", Inventory:",value[4])
        print("\n---------------------------------------------------")
        buy_index = validate_index(len(list(enumerate(rows))))
        print("\n---------------------------------------------------")
        print("\nThe chosen laptop is:")
        for index,value in enumerate(rows):
            if index+1 == buy_index:
                print(value[1],", Price:  Rs.",value[3])
                chosen_laptop = value
        print("\n---------------------------------------------------")
            
        confirm = validate_confiramtion()
        if confirm:
            quantity = validate_quantity(chosen_laptop[4])
            cursor = conn.cursor()
            # 0 pid, 1 name, 2 category, 3 price (adding data to cart table)
            cursor.execute("INSERT INTO `product_db`.`cart` (`name`, `category`, `price`, `quantity`, `total`) VALUES (%s, %s, %s,%s,%s)"
                               ,[chosen_laptop[1],chosen_laptop[2],chosen_laptop[3],quantity,chosen_laptop[3]*quantity])
            # for updating stock in product table
            cursor.execute("UPDATE `product_db`.`product` SET `stock` = '%s' WHERE (`pid` = '%s')",[chosen_laptop[4]-quantity,chosen_laptop[0]])
            conn.commit()
            print("\n---------------------------------------------------")
            print("\nLaptop Added to Cart")
            
            continued = input("Do you want to add more products? (y/Y for continuing anything else will redirect to main menu)")
            if continued == "y" or continued == "Y":
                product = Product()
            else:
                main()

        else:
            product = Product()
    else:
        print("No Laptops Available in Inventory")
        print("\n---------------------------------------------------")

def main():
    """
    Main Function, used to initiate the program. It gives options to user for buying laptop or viewing the cart.
    """
    print("\n---------------------------------------------------")
    print("Welcome to the Laptop Selling App")
    print("---------------------------------------------------\n")
    print("MENU:")
    print("\n1. BUY LAPTOP")
    print("2. CART OPTIONS")
    print("3. EXIT")
    try:
        choice = int(input("\nChoose your option: "))
        if choice == 1:
            Product()
        elif choice == 2:
            Cart()
        elif choice == 3:
            exit()
        else:
            print("Invalid Input")
            main()
    except ValueError:
        print("Invalid Input")
        main()


main()


"""
Test Cases:
Case One: Buying any category Laptop
---------------------------------------------------
Welcome to the Laptop Selling App
---------------------------------------------------

MENU:

1. BUY LAPTOP
2. CART OPTIONS
3. EXIT

Choose your option: 1

---------------------------------------------------
CATEGORIES:

---------------------------------------------------

1. Gaming Laptops
2. Work Laptops
3. Go back to main menu

Enter the category of the laptop you want to buy: 1

---------------------------------------------------
Available Laptops
---------------------------------------------------

1 : HP Omen , Price:  Rs. 85000.0 , Inventory: 53
2 : Asus ROG , Price:  Rs. 80000.0 , Inventory: 42
3 : Asus TUF , Price:  Rs. 60000.0 , Inventory: 60
4 : Lenovo LOQ , Price:  Rs. 104000.0 , Inventory: 20
5 : MSI , Price:  Rs. 100000.0 , Inventory: 2

---------------------------------------------------

Enter the index number of laptop from list: 2

---------------------------------------------------

The chosen laptop is:
Asus ROG , Price:  Rs. 80000.0

---------------------------------------------------

Are you sure? (y/n): y

---------------------------------------------------

Available Stock = 42

Enter the quantity of laptop you want to purchase: 2 

---------------------------------------------------

Laptop Added to Cart
Do you want to add more products? (y/n): y

---------------------------------------------------
CATEGORIES:

---------------------------------------------------

1. Gaming Laptops
2. Work Laptops
3. Go back to main menu

Enter the category of the laptop you want to buy:
"""