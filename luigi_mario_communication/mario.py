import requests
import json
from datetime import datetime
import time

# main program
print("\n\n*** Mario ***\n")
order = ()
appended_order = []
orders = {}
order_number = int(input("Enter Order Number"))
pizza_type = ''

print("1.Pizza Margherita")
print("2.Pizza Pepperoni")
print("3.Pizza Four Cheese")
print("4.Pizza BBQ Chicken")
print("5.Pizza Vegetarian")
print("6.Pizza Meat Lovers")

while True:

    pizza_code = input("Enter Pizza Type: (Enter to Quit) ")
    
    if pizza_code == '':
        break
    elif pizza_code == "1":
        pizza_type = 'Pizza Margherita' 
    elif pizza_code == "2":
        pizza_type = 'Pizza Pepperoni' 
    elif pizza_code == "3":
        pizza_type = 'Pizza Four Cheese' 
    elif pizza_code == "4":
        pizza_type = 'Pizza BBQ Chicken' 
    elif pizza_code == "5":
        pizza_type = 'Pizza Vegetarian' 
    elif pizza_code == "6":
        pizza_type = 'Pizza Meat Lovers' 


    pizza_quantity = int(input("Enter Pizza Quantity: "))
    
    order = (pizza_type , pizza_quantity)
    appended_order.append(order)
        
    # assign date and time of the order
    rightNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    orders = { "date and time": rightNow ,
                "order number": order_number,
                "order": appended_order }

print("Your order is: ", appended_order )   
user_input = input("Confirm Order y/n ")

if user_input == "y":
    print("Your order is confirmed")
    time.sleep(3)
else :
    print("Order is cancelled! ")
    time.sleep(3)
    orders = {}


response = requests.post('http://localhost:5000/mario_register', json = orders)


# out_file = open("sample.json")
# json.dump(orders, out_file, indent=4)
# out_file.close()
# print(orders)



