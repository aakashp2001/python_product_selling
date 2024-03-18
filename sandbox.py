# FOR PDF GENERATION:
# pip install mysql-connector-python reportlab

# FOR MYSQL CONNECTION:
# pip install mysql-connector-python

import mysql.connector
from reportlab.pdfgen import canvas

db_host="localhost"
db_user="root"
db_pswd="aakash"
db_port="3306"
conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pswd, database="product_db", port=db_port)

#------------------------------------------------------------------------#
# Product Class                                                          #
#------------------------------------------------------------------------#

class Product:
    def __init__(self):
        print("\n---------------------------------------------------")
        print("CATEGORIES:")
        print("\n---------------------------------------------------\n")
        print("1. Gaming Laptops")
        print("2. Work Laptops")
        try:
            category = int(input("\nEnter the category of the laptop you want to buy: "))
            print("\n---------------------------------------------------")
            if category == 1:
                buy_laptop("Gaming")
            elif category == 2:
                buy_laptop("Work")
            else:
                print("Invalid Input")
                product = Product()
        except ValueError:
            print("Invalid Input")
            product = Product()


class Cart:
    def __init__(self):
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
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_db.cart")
        items = cursor.fetchall()
        if items:
            line = 0
            total_price = 0
            pdf = canvas.Canvas('Order.pdf')
            pdf.setFont('Helvetica-Bold', 24)
            pdf.drawString(250, 730, "Your Order")
            pdf.setFont('Helvetica', 16)
            pdf.drawString(100, 670, "Product")
            pdf.drawString(240, 670, "Type")
            pdf.drawString(310, 670, "Unit Price")
            pdf.drawString(400, 670, "Quantity")
            pdf.drawString(475, 670, "Total")

            pdf.setFont('Helvetica', 12)
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




def validate_index(rows):
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
    confirm = input("\nAre you sure? (y/n): ")
    if confirm == "y" or confirm == "Y":
        return True
    elif confirm == "n" or confirm == "N":
        return False
    else:
        print("Invalid Input")
        return validate_confiramtion()
    
def validate_quantity(inventory):
    print("\n---------------------------------------------------")
    print("\nAvailable Stock =",inventory)
    try:
        quantity = int(input(f"\nEnter the quantity of laptop you want to purchase: "))
        if quantity > 0 and quantity <= inventory:
            return quantity
        else:
            print("\nNumber of laptop should be less than Available Stock")
            return validate_quantity(inventory)
    except ValueError:
        print("\nNumber of laptop should be less than Available Stock")
        return validate_quantity(inventory)   

def buy_laptop(category):
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM product_db.product WHERE category = %s AND stock > 0",[category])
    rows = cursor.fetchall()
    if rows:
        print("Available Laptops")
        print("---------------------------------------------------\n")
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
            cursor.execute("INSERT INTO `product_db`.`cart` (`name`, `category`, `price`, `quantity`, `total`) VALUES (%s, %s, %s,%s,%s)"
                               ,[chosen_laptop[1],chosen_laptop[2],chosen_laptop[3],quantity,chosen_laptop[3]*quantity])
            cursor.execute("UPDATE `product_db`.`product` SET `stock` = '%s' WHERE (`pid` = '%s')",[chosen_laptop[4]-quantity,chosen_laptop[0]])
            conn.commit()
            print("\n---------------------------------------------------")
            print("\nLaptop Added to Cart")
            
            continued = input("Do you want to add more products? (y/n): ")
            if continued == "y" or continued == "Y":
                product = Product()
            elif continued == "n" or continued == "N":
                main()
            else:
                print("Invalid Input")
                main()

        else:
            product = Product()
    else:
        print("No Laptops Available in Inventory")
        print("\n---------------------------------------------------")

def main():
    print("\n---------------------------------------------------")
    print("Welcome to the Laptop Selling App")
    print("---------------------------------------------------\n")
    print("MENU:")
    print("\n1. BUY LAPTOP")
    print("2. VIEW CART")
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



# For future:

# buy_laptop(category) - reuse code for both categories
# check if product already exists in cart, if yes, update number, otherwise create new row
