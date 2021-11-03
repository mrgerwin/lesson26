from guizero import App, PushButton, Text, TextBox, ListBox, Box, Window, error
import sqlite3

def openDB():
    try:
        conn = sqlite3.connect("register.db")
    except:
        error("DB Error", "Could not open the database")

    try:
        conn.execute("CREATE TABLE IF NOT EXISTS PRODUCTS (ID TEXT NOT NULL UNIQUE, NAME TEXT NOT NULL, PRICE REAL NOT NULL, QUANTITY INTEGER NOT NULL);")
        conn.execute("CREATE TABLE IF NOT EXISTS CUSTOMERS (ID TEXT NOT NULL UNIQUE, NAME TEXT NOT NULL, PHONE INTEGER NOT NULL);")
        conn.commit()
    except:
        error("DB Error", "Could not make the tables")

    return conn

def loadDBValues():
    try:
        cur = conn.cursor() 
        cur.execute("SELECT * FROM PRODUCTS")
        allProducts = cur.fetchall()
        for product in allProducts:
            Products.append(product)
        cur.execute("SELECT * FROM CUSTOMERS")
        allCustomers = cur.fetchall()
        
        for customer in allCustomers:
            Customers.append(customer)
    except:
        error("DB Error", "Error loading values from Database")

def DBStoreCustomer(customer):
    conn.execute("INSERT INTO CUSTOMERS (ID, NAME, PHONE) VALUES (?,?,?);", (customer[0], customer[1], customer[2]))
    conn.commit()
    
def DBStoreProduct(product):
    conn.execute("INSERT INTO PRODUCTS (ID, NAME, PRICE, QUANTITY) VALUES (?,?,?,?);", (product[0], product[1], product[2], product[3]))
    conn.commit()

def showCustomerWindow():
    AddCustomerWindow.show()
    idTextBox.value = CustIDTextBox.value

def AddCustomer():
    try:
        Customers.append([idTextBox.value, nameTextBox.value, int(phoneTextBox.value)])
        DBStoreCustomer([idTextBox.value, nameTextBox.value, int(phoneTextBox.value)])
        AddCustomerWindow.hide()
    except TypeError:
        error("Input Error", "Something doesn't make sense.  Try again.")
    except Exception as e:
        error("Unknown Error", e)

def AddProduct():
    try:
        Products.append([idPTextBox.value, namePTextBox.value, float(priceTextBox.value), int(quantityTextBox.value)])
        DBStoreProduct([idPTextBox.value, namePTextBox.value, float(priceTextBox.value), int(quantityTextBox.value)])
        AddProductWindow.hide()
    except TypeError:
        error("Input Error", "Something doesn't make sense.  Try again.")
    except ValueError:
        error("Input Error", "You didn't put in a number.  Try again.")
    except Exception as e:
        error("Unknown Error", e)
def showProductWindow():
    AddProductWindow.show()
    idPTextBox.value = ProductIDTextBox.value

def DisplayCustomer():
    
    for cust in Customers:
        ID = cust[0]
        if ID == CustIDTextBox.value:
            CustNameText.value = cust[1]
            CustPhoneText.value = cust[2]
            return
    else:
        CustNameText.value = "Not Found"
        CustPhoneText.value = ""

def DisplayProduct():
    global CurrentIndex
    
    CurrentIndex = 0
    for prod in Products:
        ID = prod[0]
        if ID == ProductIDTextBox.value:
            ProdNameText.value = prod[1]
            ProdCostText.value = prod[2]
            return
        else:
            CurrentIndex += 1
    else:
        ProdNameText.value = "Not Found"
        ProdCostText.value = ""
        CurrentIndex = None

def Purchase():
    global Total
    if CurrentIndex != None:
        CartListBox.append([Products[CurrentIndex][1], Products[CurrentIndex][2]])
        Total += Products[CurrentIndex][2]
        TotalText.value= "Total: $" + str(Total)
    else:
        print("No Product Selected")
MainWindow = App("Cash Register", 800, 800)

CustomerBox = Box(MainWindow, layout="grid", border = 1)
ProductBox = Box(MainWindow, layout ="grid", border = 1)
CartBox = Box(MainWindow, layout = "grid",border = 1)

CustText = Text(CustomerBox, text = "Customer ID Number", grid=[0,0])
CustIDTextBox = TextBox(CustomerBox, grid=[0,1])

EnterCustButton = PushButton(CustomerBox, text="Enter", command = DisplayCustomer, grid=[1,1])
AddCustButton = PushButton(CustomerBox, text="Add/Edit Customer", command=showCustomerWindow, grid=[2,1])
CustNameText = Text(CustomerBox, text = "Name:", grid=[0,2])
CustPhoneText = Text(CustomerBox, text = "Phone:", grid=[1,2])

EnterProductButton = PushButton(ProductBox, text="Enter", command =DisplayProduct, grid=[1,1])
ProductText = Text(ProductBox, text = "Product ID Number", grid=[0,0])
ProductIDTextBox = TextBox(ProductBox, grid=[0,1])
AddProductButton = PushButton(ProductBox, text="Add/Edit Product", command=showProductWindow, grid=[2,1])
ProdNameText = Text(ProductBox, text="Name:", grid=[0, 2])
ProdCostText = Text(ProductBox, text = "$", grid=[1,2])

PurchaseButton = PushButton(CartBox, text = "Purchase", command=Purchase, grid=[0,0])
CartListBox = ListBox(CartBox, grid=[0,1])
TotalText = Text(CartBox, text = "Total: $0.00", grid=[0,2])
CheckOutButton = PushButton(CartBox, text = "Check Out", grid = [0,3])

AddCustomerWindow = Window(MainWindow, title="Add/Edit Customer", height = 300, width = 300)
AddCustomerWindow.hide()

nameText = Text(AddCustomerWindow, text="Name: ")
nameTextBox = TextBox(AddCustomerWindow)
phoneText = Text(AddCustomerWindow, text="Phone: ")
phoneTextBox = TextBox(AddCustomerWindow)
idText = Text(AddCustomerWindow, text="ID Num: ")
idTextBox = TextBox(AddCustomerWindow)
addCButton = PushButton(AddCustomerWindow, text="Add", command=AddCustomer)


AddProductWindow = Window(MainWindow, title="Add/Edit Product", height = 300, width = 300)
AddProductWindow.hide()
namePText = Text(AddProductWindow, text="Name: ")
namePTextBox = TextBox(AddProductWindow)
priceText = Text(AddProductWindow, text="Price: ")
priceTextBox = TextBox(AddProductWindow)
quantityText = Text(AddProductWindow, text="Quantity: ")
quantityTextBox = TextBox(AddProductWindow)
idPText = Text(AddProductWindow, text="ID Num: ")
idPTextBox = TextBox(AddProductWindow)
addPButton = PushButton(AddProductWindow, text="Add", command=AddProduct)

loadDBButton = PushButton(MainWindow, text="Load DB Values", command=loadDBValues)
#Data Structures

#Customers
Customers = [["9230", "John Doe", 4192229999], ["0001","First Customer", 8886667777], ["0002", "Second Customer", 7659287162]]
#Products
Products = [["10232", "Pens Pack of 10", 2.99, 43], ["11111", "Folders", 3.99, 34], ["00001", "Pencils", .99, 24], ["92932", "Stationary", 4.99, 53]]

CurrentIndex = None
Total = 0

conn = openDB()
MainWindow.display()
conn.close()