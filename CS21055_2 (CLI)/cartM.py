import datetime

from PRODUCTSDATAFILE import productsdata
import pandas as pd
import json

class ShoppingCart:
    def __init__(self,name=''):
        self.shelf=productsdata
        self.name = name
        self.cart_items = []
        self.total_items_value = None
        self.shelf=productsdata

    def __repr__(self):                          ##overriding str method
        return f'A class for {self.name} '

    def _check_quantity(self, id, quantity):        ##items quantity check method
        called_item = [item for item in self.shelf if item['ID']==id][0]
        if quantity<=called_item['QUANTITY']:       ##checking if the quantity of the called_item is available
            return True
        else:
            return False

    def add_to_cart(self):          ##selection of products and adding into cart
        try:
            while True:
                    df = pd.DataFrame(self.shelf)           ##products into table format
                    print("\n<<< Enter ID of item you want to add to cart >>> ")
                    print(df.to_string())
                    id = int(input('''\nselect the id of the item you want to buy: \n>>> '''))
                    quantity = int(input('''How many do you want: \n>>> '''))
                    if self._check_quantity(id, quantity):
                        called_item = [item for item in self.shelf if item['ID'] == id][0]
                        called_item['QUANTITY']-=quantity
                        print('\nCATEGORY:{}\n========================\n1. NAME: {}\n2. PRICE: {}\n3. SUBCATEGORY: {}\n4. QUANTITY: {}\n5. ID: {}'.format(called_item['CATEGORY'], called_item['NAME'], called_item['PRICE'],called_item['SUBCATEGORY'], quantity, id))
                        for i in range(0,len(productsdata)):
                            if productsdata[i]["ID"] == called_item["ID"]:
                                print('Remaining Items:',called_item['QUANTITY'])
                        fname = "PRODUCTSDATAFILE.py"
                        with open(fname, 'w') as f:
                            f.write('productsdata = {}'.format(productsdata))
                            f.close()
                        self.cart_items.append(called_item)        ##adding selected items into cart
                        with open("data.json","r+") as f:           ##data extraction from json file
                            data = json.loads(f.read())
                            for i in data:
                                if data[i]['username']==self.name:
                                    id = i
                            data[id]['cart'].append({
                                'id':called_item['ID'],
                                'name':called_item['NAME'],
                                'price':called_item["PRICE"],
                                'category':called_item['CATEGORY'],
                                'subcategory': called_item['SUBCATEGORY'],
                                'quantity':quantity,
                                "date_of_purchase":str(datetime.datetime.now())
                            })

                            f.seek(0)
                            f.write(json.dumps(data,indent=4))
                            checkout = input("\nCheckout? (y/n)\n>>> ")
                            if checkout == 'y':
                                # f.seek(0)
                                # f.write(json.dumps(data,indent=4))
                                break
                            continue
                    else:
                        print("The quantity you have selected is more than stock, try again")
                        continue
        except Exception as e:
            print("An unexpected error has occurred, please try again.",e)
            self.add_to_cart()

    def view_cart(self):        ## shows the added items in cart
        with open("data.json","r") as f:
               data = json.loads(f.read())
               for i in data:
                    if data[i]['username']==self.name:
                         for n,i in enumerate(data[i]['cart']):
                            print('{}) {}'.format(n+1,i['name']))

    def remove_from_cart(self):           ## removing existing items from the cart
        while True:
            with open("data.json",'r') as f:
                data = json.loads(f.read())
                for i in data:
                        if data[i]['username']==self.name: user_id = i
                if len(data[user_id]['cart'])==0:
                    print("You don't have any items in your cart.")
                    return None
            print("Here is your cart:")
            self.view_cart()
            print('To quit type a value that is not in your cart\n>>> ')
            try:
                no = int(input('Select number of the item you want remove\n>>> '))
                with open("data.json","r+") as f:
                    data = json.loads(f.read())
                    data[user_id]['cart'].pop(no-1)
                    with open("data.json","w") as f:
                        f.write(json.dumps(data,indent=4))
            except: pass
            done = input('Do you want to continue removing from cart? (y/n)\n>>> ')
            if done == 'y':
                continue
            else:
                break
        return None