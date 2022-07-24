# from PRODUCTSDATAFILE import productsdata
from Customer import Customer
from cartM import ShoppingCart
import time
import datetime
import json
# import random
class order:
    def __init__(self,name):
        with open('data.json','r') as f:
            data=json.loads(f.read())
            for i in data:
                if name==data[i]['username']:
                    self.user_id=i
        self.cart=ShoppingCart(name)
        self.name=name
        self.order_ID=0

    def place_order(self):
        """Places Order by checking the amount in stock and update the Order History for each user"""
        while True:
            option=input("\nChoose An Option:\n 1) Add To Cart\n 2) Remove From Cart\n 3) Pay\n 4) Quit Shopping\n>>> ")
            if option=='1':
                self.cart.add_to_cart()
            elif option=='2':
                self.cart.remove_from_cart()
            elif option=='3':
                with open('data.json','r') as f:
                    data=json.loads(f.read())
                    if len(data[self.user_id]['cart'])==0:
                        print("Can't process payment procedure, requires a non-empty cart")
                    else:
                        self.payment()
            elif option=='4':
                break
    def payment(self):
        """Payment: two modes of payment with multi currency payment also have implementation for currency conversion"""
        self.total_items_value=0
        currency=input('\nEnter currency of payment: \n1) USD\n2) EUR\n3) SAR\n4) AED\n5) PKR\n>>> ')
        values=[226.65,231.12,60.31,61.71,1]
        currency_name=["USD",'EUR','SAR','AED','PKR']
        if currency in ['1','2','3','4','5']:

            with open("data.json","r") as f:
                data = json.loads(f.read())
                for i in data:
                    if self.name==data[i]['username']:
                        for i in data[i]['cart']:
                            self.total_items_value+=round(i['quantity']*(i['price']/values[int(currency)-1]),2)
        else:
            self.payment()


        print(f"\nYour total is {self.total_items_value} {currency_name[int(currency)-1]}")
        print()
        self.paymentmethod=input("Enter payment method:\n 1) Cash On Delivery\n 2) DebitCard\n>>> ")
        if self.paymentmethod=='1':
            time.sleep(5)
            print("\n\nPlease Wait !!\n\n")
            time.sleep(5)
            print("Your Order Has Been Placed")
            self.details = 'Cash on Delivery'
        elif self.paymentmethod=='2':
            print("Enter Your Details To Proceed")
            card_number=int(input("Enter Your Card Number: \n>>> "))
            expiry_month=int(input("Expiry Month: \n>>> "))
            expiry_year=int(input("Expiry Year: \n>>> "))
            card_CVV=int(input("Enter Card CVV: \n>>> "))
            input("<<< Press Enter to Proceed >>> ")
            time.sleep(6)
            print("\n\nPlease Wait !!\n\n")
            time.sleep(6)
            print("Your order Has been placed")
            print("Thanks For Shopping !!")
            self.details = {
                'card_number':card_number,
                'expiry_month':expiry_month,
                'expiry_year':expiry_year,
                'card_CVV':card_CVV
            }
        else:
            self.payment()
        self.update_records()
        with open("data.json","r") as f:
            data = json.loads(f.read())
            for i in data:
                if data[i]['username']==self.name:
                    id = i
            for j in data[id]['cart']:
                data[id]['history'].append(j)
            data[id]['cart'] = []
            with open('data.json','w') as f:
                f.write(json.dumps(data,indent=4))
    def update_records(self):
        """Records are updated in a n order details file after each order"""
        with open("orderdetails.txt","a+") as f:
            f.write(f"\n{self.name},{self.order_ID},{self.cart.cart_items},{self.total_items_value},{self.details},{datetime.datetime.now()}")
