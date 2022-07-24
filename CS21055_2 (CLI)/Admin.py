from User import User
# from PRODUCTS import products
from PRODUCTSDATAFILE import productsdata
from cartM import ShoppingCart
import pandas as pd
import json
import abc

class Admin(User):
    def __init__(self,name='',password='',email_address=''):
        super().__init__(name,password,email_address)
        self.logged_in=False
        self.shelf=productsdata
    def log_in(self):
        opt=input('\nLogin using\n 1) Username and Password\n 2) Email Address and Password\n>>> ')
        if opt=='1':
            self.name=input('\nEnter Username\n>>> ')
            self.password=input('Enter Password\n>>> ')
            if self.name=="Admin" and self.password=="123":
                self.logged_in=True
                print('Successfully Logged In')
                self.choice()
            else:
                print('\n Invalid Credentials,Please Try Again\n')
                self.log_in()
        elif opt=='2':
            self.email_address=input('\nEnter Email Address\n>>> ')
            self.password=input('Enter Password\n>>> ')
            if self.email_address=="admin123@gmail.com" and self.password=="123" :
                self.logged_in=True
                print('Successfully Logged In')
                self.choice()
            else:
                print('\nInvalid Credentials,Please Try Again\n')
                self.log_in()
        else:
            print('INVALID INPUT\n')
            import Main
            Main.login_main()


    def choice(self):
        if self.logged_in:
            while True:
                opt=input("\nEnter your choice:\n 1) View products\n 2) View customer information\n 3) Remove customer\n 4) Update products\n 5) Search Customer\n 6) Search Product\n 7) Logout\n>>> ")
                if opt=='1':
                    self.view_products()
                elif opt=='2':
                    self.view_customers()
                elif opt=='3':
                    self.delete_customer()
                elif opt=='4':
                    self.update_products()
                elif opt=='5':
                    self.search_info()
                elif opt=='6':
                    self.search_product()
                elif opt=='7':
                    print("You have logged out")
                    break
            
            import Main
            Main.login_main()
        else:
            print("Not authorized.")
            self.log_in()

    def view_products(self):
        if self.logged_in:
            from products import Products
            obj=Products()
            obj.view_products()

            # for no,i in enumerate(productsdata):
            #     print('\n{}.'.format(no+1),i,'\n')
            #     print('0. ID: {}\n1. NAME:{}\n2. PRICE:{}\n3. CATEGORY:{}\n4. SUBCATEGORY:{}\n5. QUANTITY:{}\n'.format(productsdata[i]['id'],productsdata[i]['NAME'],productsdata[i]['PRICE'],productsdata[i]['CATEGORY'],productsdata[i]['SUBCATEGORY'],productsdata[i]['QUANTITY']))
            self.choice()
        else:
            print("Not authorized.")

    
    def view_customers(self):
        if self.logged_in:
            print('\n')
            with open('data.json','r') as f:
                data = json.loads(f.read())
                for n in data:
                    print(f"ID: {n}\nUSERNAME: {data[n]['username'].upper()}\nPASSWORD: {data[n]['password']}\n EMAIL ADDRESS: {data[n]['email_address']}\nADDRESS: {data[n]['address']}\nMOBILE NUMBER: {data[n]['mobile_no']}\nGENDER: {data[n]['gender']}\nCART: {data[n]['cart']}\nHISTORY: {data[n]['history']}\n\n")
                print('>>> TOTAL NUMBER OF CUSTOMERS: {}'.format(len(data)))
        else:
            print("Not authorized.")

    def update_products(self):
        if self.logged_in:
            df = pd.DataFrame(self.shelf)
            print(df.to_string())
            add_remove=input('\nDo you want to:\n1) Add Products\n2) Remove Products\n>>> ')
            if add_remove=='1':
                from products import Products
                obj=Products()
                obj.add_products()
            if add_remove=='2':
                from products import Products
                obj = Products()
                obj.remove_items()
            else:
                print('Invalid Input')
                self.update_products()

        else:
            print('Not Authorized')

    def delete_customer(self):
        try:
            if self.logged_in:
                with open('data.json','r') as f:
                    data=json.loads(f.read())
                    self.view_customers()
                    try:
                        id = int(input("\nEnter ID number of user\n>>> "))
                    except: pass
                    data.pop(str(id))
                    with open('data.json','w') as file:
                        file.write(json.dumps(data,indent=4))
            else:
                print('Not Authorized')
        except:
            print("An unexpected error occurred.")

    def search_info(self):
        if self.logged_in:
            query_list=[]
            with open('data.json','r') as f:
                data=json.loads(f.read())
                query = input("Enter query:\n>>> ")
                for i in data:
                    user_info=list(data[i].values())
                    if query in user_info[0]:
                        query_list.append(user_info)


                if query_list==[]:
                    print('No results were found')
                else:
                    print(f"found {len(query_list)} result(s)")
                    for i in query_list:
                        print('1. NAME:{}\n2. PASSWORD:{}\n3. EMAIL ADDRESS:{}\n4. ADDRESS:{}\n5. GENDER:{}\n6. MOBILE NUMBER:{}\n7. BIRTH DATE:{}\n8. CART:{}\n9. HISTORY:{}\n\n'.format(i[0], i[1], i[2], i[3], i[4], i[5],i[6], i[7], i[8]))
        else:
            print('Not Authorized')

    def search_product(self):
        opt = input("\n 1) Search by Category\n 2) Search by Product\n 3) Search by Subcategory\n 4) Search by Price\n 5) Search by Quantity\n>>> ")
        found = []
        available=False
        try:
            if opt == "1":
                print('\nThe following categories are available:\n ELECTRONICS\n VIDEO GAMES\n BOOKS\n MOVIES&TV\n MUSIC\n')
                category = input("\nEnter Category:\n>>> ").upper()
                for i in productsdata:
                    if category in i['CATEGORY']:
                        available=True
                if available==False:
                    print("\nNo category was found, please try again.")
                    self.search_product()

                search=input("What are you searching for:\n>>> ").upper()
                for i in productsdata:
                    if search in i['NAME'] and category in i['CATEGORY']:
                        found.append(i)
                if found==[]:
                    print('No results')
                else:
                    print(f"\nfound {len(found)} result(s)")
                    for i in found:
                            print('\nCATEGORY:{}\n========================\n1. NAME: {}\n2. PRICE: {}\n3. SUBCATEGORY: {}\n4. QUANTITY: {}\n'.format(i['CATEGORY'], i['NAME'], i['PRICE'],i['SUBCATEGORY'], i['QUANTITY']))
                
            elif opt == "2":
                search=input('\nSEARCH by Name:\n>>> ').upper()
                for i in productsdata:
                    if search in i['NAME']:
                        found.append(i)
                if found==[]:
                    print('No results')
                else:
                    print(f"\nfound {len(found)} result(s)")
                    for i in found:
                            print('\nCATEGORY:{}\n========================\n1. NAME: {}\n2. PRICE: {}\n3. SUBCATEGORY: {}\n4. QUANTITY: {}\n'.format(i['CATEGORY'], i['NAME'], i['PRICE'],i['SUBCATEGORY'], i['QUANTITY']))

            elif opt == "3":
                print("\nThe following sub-categories are included:\n LAPTOPS\n SMARTPHONES\n COMPUTERS\n SMART TV\n XBOX\n NINTENDO\n ARCADE\n VR\n E-BOOKS\n MAGAZINE\n COMICS\n COOKBOOKS")
                sub_category = input("\nEnter Sub-Category:\n>>> ").upper()
                for i in productsdata:
                    if sub_category in i['SUBCATEGORY']:
                        available=True
                if available==False:
                    print("\nNo subcategory was found, please try again.")
                    self.search_product()

                search=input('What are you searching for:\n>>> ').upper()
                for i in productsdata:
                    if search in i['NAME'] and sub_category in i['SUBCATEGORY']:
                        found.append(i)
                if found==[]:
                    print('No results')
                else:
                    print(f"\nfound {len(found)} result(s)")
                    for i in found:
                            print('\nSUBCATEGORY:{}\n========================\n1. NAME:{}\n2. PRICE:{}\n3. CATEGORY:{}\n4. QUANTITY:{}\n'.format(i['SUBCATEGORY'], i['NAME'], i['PRICE'],i['CATEGORY'], i['QUANTITY']))

            elif opt == "4":
                search=int(input('SEARCH by range of Prices:\n>>> '))
                for i in productsdata:
                    if search>=i['PRICE']:
                        found.append(i)
                if found==[]:
                    print('No results')
                else:
                    print(f"\nfound {len(found)} result(s) in the range of {search}")
                    for i in found:
                            print('\nPRICE:{}\n========================\n1. NAME:{}\n2. CATEGORY:{}\n3. SUBCATEGORY:{}\n4. QUANTITY:{}\n'.format(i['PRICE'], i['NAME'], i['CATEGORY'],i['SUBCATEGORY'], i['QUANTITY']))

            elif opt == "5":
                quantity = int(input("\nSEARCH by range of Quantities:\n>>> "))
                for i in productsdata:
                    if quantity>=i['QUANTITY']:
                        found.append(i)
                if found==[]:
                    print('No results')
                else:
                    print(f"\nfound {len(found)} result(s) for products in the range of {quantity}")
                    for i in found:
                            print('\nQUANTITY:{}\n========================\n1. NAME:{}\n2. CATEGORY:{}\n3. SUBCATEGORY:{}\n4. PRICE:{}\n'.format(i['QUANTITY'], i['NAME'], i['CATEGORY'],i['SUBCATEGORY'], i['PRICE']))

        except Exception as e:
            print("An exception occurred.", e)