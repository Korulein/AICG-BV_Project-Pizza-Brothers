import requests
import json
from datetime import datetime

order = ()
appended_order = []
orders = {}
order_number = 201
pizza_type = ''

def generate_order(order_number):
    
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
    else :
        print("Order is cancelled! ")
        orders = {}
    
    return orders
        


# main program

while True:

    print("\n\n*** Mario ***\n")

    print("1.Pizza Margherita")
    print("2.Pizza Pepperoni")
    print("3.Pizza Four Cheese")
    print("4.Pizza BBQ Chicken")
    print("5.Pizza Vegetarian")
    print("6.Pizza Meat Lovers")

    orders = generate_order(order_number)
    order_number+=1
   
    response = requests.post('http://localhost:5000/mario_register', json = orders)

    order = ()
    appended_order = []
    orders = {}

    input("Press Enter to make another order")

