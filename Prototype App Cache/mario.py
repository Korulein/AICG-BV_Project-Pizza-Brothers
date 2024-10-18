import requests
import json

# main program
print("\n\n*** Mario ***\n")
order = []
appended_order = []
orders = {}
order_number = 101
def enter_order():
    global order, orders
    while True:
     pizza_type = input("Enter Pizza Type: (Enter to Quit)")
     if pizza_type == '':
        return orders

     pizza_quantity = int(input("Enter Pizza Quantity: "))
    
     order = (pizza_type , pizza_quantity)
     appended_order.append(order)
        
    
    
     orders = { "order number": order_number,
               "order": appended_order }

def send_luigi():
 global orders, appended_order
 with open("orders.json", "r") as file:
    try:
     orderlist=json.load(file)
    except json.JSONDecodeError:
        orderlist = []  # Initialize an empty list if file is empty or invalid
 orderlist.append(orders)
 out_file = open("orders.json","w")
 json.dump(orderlist, out_file, indent=4)
 orders.clear()
 appended_order.clear()

 return True

while True:
   orders=enter_order()
   order_number+=1
   if orders== {}:
      break 
   else :
      send_luigi()
      print(orders)


