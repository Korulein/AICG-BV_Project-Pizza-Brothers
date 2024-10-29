import requests
import json

# main program
print("\n\n*** Mario ***\n")
order = []
appended_order = []
orders = {}
order_number = 101

while True:
    pizza_type = input("Enter Pizza Type: (Enter to Quit)")
    if pizza_type == '':
        
        break

    pizza_quantity = int(input("Enter Pizza Quantity: "))
    
    order = (pizza_type , pizza_quantity)
    appended_order.append(order)
        
    
    
    orders = { "order number": order_number,
               "order": appended_order }
   
out_file = open("sample.json")
json.dump(orders, out_file, indent=4)
out_file.close()
print(orders)


