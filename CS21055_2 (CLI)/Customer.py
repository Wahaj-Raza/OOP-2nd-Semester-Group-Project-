from datetime import datetime
#from itertools import product
from User import User
from cartM import ShoppingCart
from PRODUCTSDATAFILE import productsdata
import pandas as pd
import json, abc

class Customer(User):           ## user as customer method
    def __init__(self,name='',password='',email_address='',gender='',mobile_no=0,birth_date=''):
        super().__init__(name,password,email_address)
        self.gender = gender
        self.mobile_no = mobile_no
        self.birth_date = birth_date
        #MyCart=ShoppingCart()

    def choice(self):           ## choice of customer method
        from order import order
        choice = input(f"""
Hi {self.name.capitalize()} !!
Enter your Choice:
 1) View Products
 2) Logout 
 3) Shop
 4) My Orders
 5) Previous Order History
>>> """)
        if choice == '1':           ## this choice viewing the available products to the customer
            print()
            from products import Products
            obj = Products()
            obj.view_products()
        elif choice=='2':               ## logging out
            print("You are Logged Out")
            import Main
            Main.login_main()
        elif choice=='3':               ## customer placed order
            user_order=order(self.name)
            user_order.place_order()
        elif choice=='4':               ## orders placed check method
            with open("data.json","r") as f:
                data = json.loads(f.read())
                for i in data:
                    if data[i]['username']==self.name:
                        if len(data[i]['cart'])==0:
                            print("You currently have no orders in your cart")
                        else:
                            for i in data[i]['cart']:
                                print('\nCATEGORY:{}\n========================\n1. NAME: {}\n2. PRICE: {}\n3. SUBCATEGORY: {}\n4. QUANTITY: {}\n'.format(i['category'], i['name'], i['price'],i['subcategory'], i['quantity']))
                
        elif choice=='5':               ## order history check
            with open("data.json","r") as f:
                data = json.loads(f.read())
                for i in data:
                    if data[i]['username']==self.name:
                        if len(data[i]['history'])==0:
                            print("There are currently no items in your history")
                        else:
                            for i in data[i]['history']:
                                print('\nCATEGORY:{}\n========================\n1. NAME: {}\n2. PRICE: {}\n3. SUBCATEGORY: {}\n4. QUANTITY: {}\n'.format(i['category'], i['name'], i['price'],i['subcategory'], i['quantity']))
        self.choice()

    def viewproducts(self):         ## viewing products
        from products import Products
        obj=Products()
        obj.view_products()


    def login_reg(self):            ## user as customer login or register method
        option=input('\nDo you want to:\n L) Login\n R) Register\n>>> ').upper()
        if option=='R':
            self.register()
        elif option=='L':
            self.log_in()
        else:
            self.login_reg()

    def check_name(self):       ## username check method
        if len(self.name.replace(" ",''))==0:
            print("This is an invalid username, please try again")
            return "Invalid"
        with open('data.json','r') as f:
            data = json.loads(f.read())
            for i in data:
                if data[i]['username']==self.name:
                    return 'Exists'
            return 'Valid'

    def register(self):         ## non registered customers or users method
            with open('data.json','r+') as file:
                data = json.loads(file.read())
                self.name=input('\nEnter Username:\n>>> ')
                self.password=input('Enter Password:\n>>> ')
                if self.check_name()=='Valid':
                    print('\n PLEASE ENTER THE FOLLOWING INFORMATION:\n')
                    self.email_address=input('Please Enter Your Email Id:\n>>> ')
                    while '@gmail.com' not in self.email_address.lower():
                        self.email_address=input('Invalid E-mail, Enter Again:\n>>> ')
                    self.address=input('Please Enter Your Address:\n>>> ')
                    self.gender=input('Please Enter Your Gender (F/M):\n>>> ')
                    while self.gender.upper() not in ['M','F']:
                        self.gender = input("Invalid Gender, Enter Again:\n>>> ")
                    if self.gender.upper()=="F": self.gender='Female'
                    elif self.gender.upper()=="M": self.gender='Male'
                    self.mobile_no=input('Enter Your Mobile Number:\n>>> ')
                    while True:     ## validity check
                        try:
                            while len(str(self.mobile_no))!=11:
                                self.mobile_no=input('Invalid Mobile Number, Enter Again:\n>>> ')
                            int(self.mobile_no)
                            break
                        except: pass
                        self.mobile_no=input('Invalid Mobile Number, Enter Again:\n>>> ')
                    self.birth_date=input('Enter Your Birth Date (DD/MM/YYYY):\n>>> ')
                    while True:
                        try:
                            datetime(int(self.birth_date.split("/")[-1]),int(self.birth_date.split("/")[-2]),int(self.birth_date.split("/")[-3]))
                            if int(self.birth_date.split("/")[-1])>=1900: break
                        except: pass
                        self.birth_date=input('Invalid Date, Enter Again (DD/MM/YYYY):\n>>> ')
                    data.update({
                        f"{int(list(data)[-1])+1}":{
                            "username":self.name,
                            "password":self.password,
                            "email_address":self.email_address,
                            "address":self.address,
                            "gender":self.gender,
                            "mobile_no":self.mobile_no,
                            "birth_date":self.birth_date,
                            "cart":[],
                            "history":[]
                        }
                    })
                    with open('data.json',"w")as f:
                        f.write(json.dumps(data,indent=4))
                    print("Successfully registered {}".format(self.name.upper()))
                    self.login_reg()
                else:
                    print('The account could not be created')
                    import Main
                    Main.login_main()
    def log_in(self):           ##registered users or customers login method
        login =input('\nLogin Using\n 1) Username or Password\n 2) Email Address or Password\n>>> ')
        if login=='1':
            self.name = input('\nEnter Username:\n>>> ')
            self.password = input('Enter Password:\n>>> ')
            with open('data.json','r') as file:
                data = json.loads(file.read())
                for i in data:
                    if data[i]['username']==self.name and data[i]['password']==self.password:
                        print("\nLogin Successful.")
                        self.choice()
                        return True
                print("Invalid credentials, please enter again.")
                self.login_reg()
                return False
        elif login=='2':
            self.email_address= input('\nEnter Email:\n>>> ')
            self.password = input('Enter Password:\n>>> ')
            with open('data.json','r') as file:
                data = json.loads(file.read())
                for i in data:
                    if data[i]['email_address']==self.email_address and data[i]['password']==self.password:
                        self.name=data[i]['username']
                        print("\nLogin Successful.")
                        self.choice()
                        return True
                print("Invalid credentials, please enter again.")
                self.login_reg()
                return False
        else:
            print('INVALID INPUT\n')
            import Main
            Main.login_main()
