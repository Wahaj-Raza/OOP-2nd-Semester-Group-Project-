from PRODUCTSDATAFILE import productsdata
import pandas as pd

class Products:
    def __init__(self, total=0, items={}):
        self.total = total
        self.items = items
#this class is used to store and execute the data and functions realated to the products


    def update_products(self, product_id, product_type, product_name, quantity, price):
        self.product_type = product_type
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.product_id = product_id
        self.items.update({product_name: quantity})
        print(self.items)
    #this method is used to update the products by taking the user defined attributes and print the update list of products stored in dictionary format when required

    def view_products(self):
        df = pd.DataFrame(productsdata)
        print(df.to_string())
    #this method simply prints the products in table format, method of panda library is used.

    def remove_items(self):
        try:
            self.view_products()
            id=int(input('\nEnter the ID of the item you want to remove\n>>> '))
            called_item=[item for item in productsdata if item['ID']==id][0]
            productsdata.remove(called_item)
            with open('PRODUCTSDATAFILE.py','w') as f:
                f.write('productsdata={}'.format(productsdata))
        except Exception as e:
            print("An unexpected error occurred",e)
    #this function removes the product that was previously stored in file by taking id as an input,as soon as the id is given the functions calls the item of given id in the file and simplyremoves the specified product
    #expection is used to print to prevent any abnormal termination of a program

    def add_products(self):
            id = productsdata[-1]['ID'] + 1
            while True:
                name = input('Enter the name of the product:\n>>> ').upper()
                try:
                    if True in [i['NAME']==name for i in productsdata]:
                        print('ALREADY EXISTS')
                        continue
                    int(name)
                    print('INVALID INPUT')
                except:
                    break

            while True:
                try:
                    price = int(input('Enter the price of the product:\n>>> '))
                    break

                except:
                    print('INVALID INPUT')

            while True:
                category = input('Enter product category:\n>>> ').upper()
                try:
                     int(category) or float(category)
                     print('INVALID INPUT')
                except:
                    break

            while True:
                subcategory = input('Enter product sub-category:\n>>> ').upper()
                try:
                    int(subcategory) or float(subcategory)
                    print('INVALID INPUT')
                except:
                    break
            while True:
                try:
                    quantity = int(input('Enter product quantity:\n>>> '))
                    break
                except:
                    print('INVALID INPUT')



            productsdata.append({'ID':id ,'NAME': name, 'PRICE': price, 'CATEGORY': category, 'SUBCATEGORY': subcategory, 'QUANTITY': quantity})
            with open('PRODUCTSDATAFILE.py','w') as f:
                f.write('productsdata={}'.format(productsdata))
            print('THE UPDATED LIST OF PRODUCTS IS AS FOLLOWS\n ')
            self.view_products()


    #this function takes the name of the product and if name salready exists it simply prints that it already exists whereas
    #all the details of products are inputted to add it into the file if it doesnot already exists
    #expections are used to print to prevent any abnormal termination of a program


    def search_product(self):
        print('BROWSE DEPARTMENTS')
        opt = input("1. Search by category\n2. Search by product\n")
        found = []
        try:
            if opt == "1":
                category = input("What are you searching for: ").upper()
                for i in productsdata:
                    if category == productsdata[i]['CATEGORY']:
                        j = (productsdata[i])
                        print(
                            'CATEGORY:{}\n========================\n1. NAME:{}\n2. PRICE:{}\n3. SUBCATEGORY:{}\n4. QUANTITY:{}\n'.format(
                                j['CATEGORY'], j['NAME'], j['PRICE'], j['SUBCATEGORY'], j['QUANTITY']))
                print('found {} result(s)'.format(len(j)))
                search = input('What are you searching for').upper()
                for i in productsdata:
                    if search in productsdata[i]['NAME']:
                        found.append(productsdata[i])
                if found == []:
                    print('No results')
                else:
                    for i in found:
                        print('1. NAME:{}\n2. PRICE:{}\n3. SUBCATEGORY:{}\n4. QUANTITY:{}\n'.format(i['CATEGORY'],
                                                                                                    i['NAME'],
                                                                                                    i['PRICE'],
                                                                                                    i['SUBCATEGORY'],
                                                                                                    i['QUANTITY']))
                    print("found {} result(s)".format(len(found)))
            elif opt == "2":
                search = input('What are you searching for:').upper()
                for i in productsdata:
                    if search in productsdata[i]['NAME']:
                        found.append(productsdata[i])
                if found == []:
                    print('No results')
                else:
                    for i in found:
                        print('1. NAME:{}\n2. PRICE:{}\n3. CATEGORY:{}\n3. SUBCATEGORY:{}\n4. QUANTITY:{}\n'.format(
                            i['NAME'], i['PRICE'], i['CATEGORY'], i['SUBCATEGORY'], i['QUANTITY']))
                    print("found {} result(s)".format(len(found)))

        except:
            print("An exception occurred.")
    #this function searches the product on the basis of option chosen by the user
    #expections are used to print to prevent any abnormal termination of a program
    #for loop is used to search for the product in the stored file
    #if the desired product is not found suitable message will be printed on screen
    #if the similar named or category product exists,it will show the number of of results of the search while showing them all on the screen

    def checkout(self, amount_paid):
        self.amount_paid = amount_paid

        if self.amount_paid >= self.total:
            print('amount to be returned is:', self.amount_paid - self.total)
            print('THANKYOU FOR SHOPPING!')
        else:
            return "The amount paid is not adequate"
        quit()
    #the amount paid is rechecked if it is more than the required,balance amounted is printed on the screen
    #and if the amount is not adequate an approriate message is printed
    #the built-in quit() function is used to exit the program within an interpreter
