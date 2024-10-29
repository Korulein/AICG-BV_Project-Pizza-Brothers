import requests

order_in_preparation = {}

def what_to_do():
    action = input("Take an order? (Y/N) ")

    if action in "Yy":
        return "y"
    elif action in "Nn":
        return "n"
    else:
        print("Invalid option (only Y/N).")
        return ""

def take_an_order():
    
    response = requests.get('http://localhost:5000/take')
    data = response.json()

    if data == {}:
        print("No orders at the server.")
        return

    date = data['date']
    order_number = data['order_number']
    order_details = data['order_details']

    print("Order received from server: ", date, order_number,order_details)
    return data

# main program
print("\n\n*** Luigi ***\n")    

while True:
    action = what_to_do()

    if action == "y":
        order_in_preparation = take_an_order()
        print(order_in_preparation)
        response = requests.post('http://localhost:5000/luigi_register', json = order_in_preparation)

    elif action == "n":
        break
