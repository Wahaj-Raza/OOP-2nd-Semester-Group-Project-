""""MAIN FILE"""
from Customer import Customer
from Admin import Admin
from cartM import ShoppingCart
from order import order
from PRODUCTSDATAFILE import productsdata
import pandas as pd
import json

def login_main():
     admin_customer=input("\nAre you:\n 1) Admin\n 2) Customer\n>>> ")
     if admin_customer=='1':
          user = Admin()
          user.log_in()
     elif admin_customer=='2':
          user = Customer()
          user.login_reg()
     else:
          login_main()
    #admin_customer is used as a variable to take input from the user whether to choose admin or customer
if __name__=='__main__':
     print("Welcome to our Shopping App")
     login_main()
     #this function prints the welcome greeting as soon  as the application runs