import mysql.connector

db_host="localhost"
db_user="root"
db_pswd="aakash"

conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pswd, database="product_db")

#------------------------------------------------------------------------#
# Product Class                                                          #
#------------------------------------------------------------------------#

class Product:
    def __init__(self):
        print("\n---------------------------------------------------\n")
        print("CATEGORIES:")
        print("1. Gaming Laptops")
        print("2. Work Laptops")
        category = int(input("\nEnter the category of the laptop you want to buy: "))
        print("\n---------------------------------------------------")
        if category == 1:
            self.list_gaming()
        elif category == 2:
            self.list_work()
        else:
            print("Invalid Input")
            product = Product()


    def list_gaming(self):
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM product_db.product WHERE category = %s AND stock > 0",["Gaming"])
        rows = cursor.fetchall()
        if rows:
            print("Available Laptops")
            print("---------------------------------------------------\n")
            for index,value in enumerate(rows):
                print(index+1,":",value[1],", Price:",value[3],", Inventory:",value[4])
            print("\n---------------------------------------------------")

            buy_index = validate_index(len(list(enumerate(rows))))
            print("\n---------------------------------------------------")
            print("\nThe chosen laptop is:")
            for index,value in enumerate(rows):
                if index+1 == buy_index:
                    print(value[1],", Price:",value[3])
                    chosen_laptop = value
            print("\n---------------------------------------------------")
            
            confirm = validate_confiramtion()
            if confirm:
                quantity = validate_quantity(chosen_laptop[4])
                print(chosen_laptop[1],chosen_laptop[2],chosen_laptop[3])
                cursor = conn.cursor()
                cursor.execute("INSERT INTO `product_db`.`cart` (`name`, `category`, `price`, `quantity`, `total`) VALUES (%s, %s, %s,%s,%s)"
                               ,[chosen_laptop[1],chosen_laptop[2],chosen_laptop[3],quantity,chosen_laptop[3]*quantity])
                cursor.execute("UPDATE `product_db`.`product` SET `stock` = '%s' WHERE (`pid` = '%s')",[chosen_laptop[4]-quantity,chosen_laptop[0]])
                conn.commit()
                print("\n---------------------------------------------------")
                print("\nLaptop Added to Cart")
            
            else:
                product = Product()
        else:
            print("No Laptops Available in Inventory")
            print("\n---------------------------------------------------")

    
    def list_work(self):
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM product_db.product WHERE category = %s AND stock > 0",["Work"])
        rows = cursor.fetchall()
        if rows:
            print("Available Laptops")
            print("---------------------------------------------------\n")
            for index,value in enumerate(rows):
                print(index+1,":",value[1],", Price:",value[3],", Inventory:",value[4])
            print("\n---------------------------------------------------")

            buy_index = validate_index(len(list(enumerate(rows))))
            print("\n---------------------------------------------------")
            print("\nThe chosen laptop is:")
            for index,value in enumerate(rows):
                if index+1 == buy_index:
                    print(value[1],", Price:",value[3])
            print("\n---------------------------------------------------")
            confirm = validate_confiramtion()
            print(confirm)
        else:
            print("No Laptops Available in Inventory")
            print("\n---------------------------------------------------")

class Cart:
    def show_cart(self):
        print("\n---------------------------------------------------")
        print("\nCART")
        print("\n---------------------------------------------------")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_db.cart")
        items = cursor.fetchall()
        if items:
            for index,value in enumerate(items):
                print(index+1,":",value)



def validate_index(rows):
    row_index = int(input("\nEnter the index number of laptop you want to purchase: "))
    if row_index > 0 and row_index <= rows:
        return row_index
    else:
        print("Invalid Input")
        return validate_index(rows)
    
def validate_confiramtion():
    confirm = input("\nAre you sure you want to purchase this laptop? (y/n): ")
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
    quantity = int(input(f"\nEnter the quantity of laptop you want to purchase:"))
    if quantity > 0 and quantity <= inventory:
        return quantity
    else:
        print("\nNumber of laptop should be less than Available Stock")
        return validate_quantity(inventory)
    

product = Product()



# For future:

# buy_laptop(category) - reuse code for both categories
# check if product already exists in cart, if yes, update number, otherwise create new row

#cursor.execute("UPDATE product_db.product SET stock = stock - 1 WHERE id = %s", [value[0]])
#conn.commit()
#print("Laptop Purchased")