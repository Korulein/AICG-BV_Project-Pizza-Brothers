import requests

order_is_cooked = {}

def what_to_do():
    action = input("pick an order to cook from preparation? y/n ")
   
    if action in "Yy":
        return "y"
    elif action in "Nn":
        return "n"
    else:
        print("Invalid option (only Y/N).")
        return ""

def prepare_an_order():
    

    response = requests.get('http://localhost:5000/cook')
    data = response.json()

    if data == {}:
        print("No orders at the server.")
        return

    date = data['date']
    order_number = data['order_number']
    order_details = data['order_details']

    print("Order received from server: ", date, order_number,order_details)
    return data




while True:
    action = what_to_do()

    if action in "Yy":
        order_is_cooked = prepare_an_order()
        print(order_is_cooked)
        response = requests.post('http://localhost:5000/smart_oven_register', json = order_is_cooked)
    else :
        break