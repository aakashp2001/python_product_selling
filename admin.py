import mysql.connector
# config variable according to your database
db_host="localhost"
db_user="root"
db_pswd="abcd"
db_port="3307"
conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pswd, database="product_db", port=db_port)
class Admin():
    """
    Consist of admin related methods.
    """
    def __init__(self):
        """
            Initializes Admin object. It gives options for admin related operations.
        """
        print("-----------Admin Dashboard------------")
        print("Select Operation to manage inventory:")
        print("1. Add New Product")
        print("2. Restock/Add Stock to Any Product")
        print("3. Change Price")
        choice = input("Enter Your Choice (anything else will log you out):")
        if choice == "1":
            self.new_product()
        elif choice == "2":
            self.update_stock()
        elif choice == "3":
            self.update_price()
        else:
            pass
    
    def new_product(self):
        """
        Takes name, category, price and stock as input from admin and inserts these data in dataabse to create new product.
        """
        try:
            print("\n---------------------------------------------------")
            name = input("Enter Name Of The Product:")
            category = None
            while True:
                category = input("""Enter Category
1. Gaming
2. Work:""")
                if category == "1":
                    category = "Gaming"
                    break
                elif category == "2":
                    category = "Work"
                    break
                else:
                    print("Invalid Input.")
            price = float(input("Enter Price of the Product:")) 
            stock = int(input("Enter Stock of the product:"))
            cur = conn.cursor()
            cur.execute("insert into product_db.product (name,category,price,stock) values (%s,%s,%s,%s)",(name,category,price,stock))
            print("Successfully added the product.")
            print("\n---------------------------------------------------")
        except ValueError as e:
            print("Wrong Input Given somewhere please try again")
            self.new_product()
        except Exception as e:
            print(e)
            self.__init__()
        finally:
            cur.close()
            conn.commit()
            self.__init__()

    def update_stock(self):
        """
        Dislpays available product then asks user to select a product. After selecting, quantity of products to add in stock is asked.
        Quantity then will be ubdated in the database after validation of quantity input.
        """
        try:
            print("""select laptop to restock""")
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM product_db.product")
            rows = cursor.fetchall()
            if rows:
                print("List of Laptops")
                print("---------------------------------------------------\n")
                for index,value in enumerate(rows):
                    print(index+1,":",value[1],", Price:  Rs.",value[3],", Inventory:",value[4])
                print("\n---------------------------------------------------")
                selected_index = self.validate_index(len(list(enumerate(rows))))
                print("\n---------------------------------------------------")
                item = rows[selected_index - 1]
                stock = int(input("Enter amount of stock to be added: "))
                if stock > 0:
                    cursor.execute("update product_db.product set stock = stock + %s where pid = '%s'",(stock,item[0]))
                    print("Restock Successfully")
                print("\n---------------------------------------------------")
        finally:
            conn.commit()
            cursor.close()
            self.__init__()

    def update_price(self):
        """
        Dislpays available product then asks user to select a product. After selecting, new price of that product is asked.
        Price then will be ubdated in the database after validation of price input.
        """
        try:
            print("\n---------------------------------------------------")
            print("""select laptop for changing price:""")
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM product_db.product")
            rows = cursor.fetchall()
            if rows:
                print("List of Laptops")
                print("---------------------------------------------------\n")
                for index,value in enumerate(rows):
                    print(index+1,":",value[1],", Price:  Rs.",value[3],", Inventory:",value[4])
                print("\n---------------------------------------------------")
                selected_index = self.validate_index(len(list(enumerate(rows))))
                print("\n---------------------------------------------------")
                item = rows[selected_index - 1]
                price = float(input("Enter amount of stock to be added"))
                if price > 0:
                    cursor.execute("update product_db.product set price = %s where pid = '%s'",(price,item[0]))
                    print("Price Changed Successfully")
                print("\n---------------------------------------------------")
                
        finally:
            conn.commit()
            cursor.close()
            self.__init__()

    def validate_index(self,rows):
        """
        Takes input from the user from the list and validates for correct row.

        Parameters:
            rows (list): Consist of list of laptops.

        Returns:
            row_index (int): index of the selected laptop.
        """
        try:
            row_index = int(input("\nEnter the index number of laptop from list: "))
            if row_index > 0 and row_index <= rows:
                return row_index
            else:
                print("Invalid Input")
                return self.validate_index(rows)
        except ValueError:
            print("Invalid Input")
            return self.validate_index(rows)

# Initializing admin object

Admin()