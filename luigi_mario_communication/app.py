from flask import Flask, render_template, request, redirect, session 
from datetime import datetime
from flask_bcrypt import Bcrypt
from functools import wraps
import requests
import time
app = Flask(__name__)
bcrypt = Bcrypt(app)
quantity = []
data = []
datas = []
preparation = []
cooked = []
pizzas_per_order=[]
pizzas_per_order_STATUS=[]
order_number = 101
global user
global login_chances
login_chances = 3

# Dictionary for pizza prices
PIZZA_PRICES = {
    'Pizza Cheese': 8.00,
    'Pizza Pepperoni': 10.00,
    'Pizza Hawaiian': 9.50,
    'Pizza Meat Lover': 12.00,
    'Pizza Shoarma': 11.50,
    'Pizza BBQ and Bacon': 10.50
}

# Dictionary for drink prices
DRINK_PRICES = {
    'Coca Cola': 3.50,
    'Coca Cola Zero': 3.50,
    'Sprite': 3.50,
    'Sprite Zero': 3.50,
    'Fuze Tea': 3.50,
    'Water': 2.50
}

users = {
    "Mario_Admin": bcrypt.generate_password_hash("J*&Hsan!aZ=+1").decode('utf-8'),
    "Luigi_Admin": bcrypt.generate_password_hash("Password123").decode('utf-8'),
}

app.secret_key = 'awuir780wtr6wesgydfhv'

login_chances = 3  # Set initial login chances
user = None

def login_required(f):
    """Decorator to check if user is logged in."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect('/error_login')  # Redirect to error page if not logged in
        return f(*args, **kwargs)
    return wrapped


def generate_order(clock, order_number, order_details, payment_method):
    global datas, pizzas_per_order,pizzas_per_order_STATUS
    pizzacounter=[]
    total_price = sum(
        (PIZZA_PRICES.get(item, 0) if item in PIZZA_PRICES else DRINK_PRICES.get(item, 0)) * int(qty)
        for item, qty in order_details
    )
    #filter to only get how many pizzas are in each order
    for item in order_details:
        print("item",item)
        if "pizza" in item[0]:
         pizzacounter.append(item[1])
    pizzas_per_order.append(sum(pizzacounter))
    pizzas_per_order_STATUS.append("waiting")
    pizzacounter.clear()
    print(pizzas_per_order,pizzas_per_order_STATUS)
            
             
    datas.append((clock, order_number, order_details, total_price, payment_method, "Waiting", dine_option))

    # Print to check if dine_option is captured
    print(f"Order Number: {order_number}, Dine Option: {dine_option}")


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect('/')  # Redirect to home page after logging out

@app.route('/error_login')
def error_login():
    return render_template('error_login.html')

@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/ordering')
def main_page():
    return render_template("ordering.html")

@app.route('/drinks')
def order_drinks_page():
    return render_template("drinks.html")

@app.route('/create_order')
def create_order():
    dine_option = request.args.get('dine_option', 'Take away')  # Default to "Take away" if not provided
    session['dine_option'] = dine_option  # Store in session to persist for the order
    return render_template("create_order.html")


@app.route('/corderconfirmation')
def order_confirmation():
    return render_template("orderconfirmation.html")

@app.route('/welcome_website')
def welcome_website():
    return render_template ("welcome_website.html")

@app.route('/register_order', methods=['POST'])
def register_order():
    currentOrders = []
    pizzacounter=[]
    global order_number, data, datas,pizzas_per_order,pizzas_per_order_STATUS  

    # Process selected pizzas
    selected_pizzas = request.form.getlist('pizza')
    # Extract quantities from the form
    quantities = {
        'Pizza Cheese': request.form.get('quantity_Cheese'),
        'Pizza Pepperoni': request.form.get('quantity_Pepperoni'),
        'Pizza Hawaiian': request.form.get('quantity_Hawaiian'),
        'Pizza Meat Lover': request.form.get('quantity_Meatlover'),
        'Pizza Shoarma': request.form.get('quantity_Shoarma'),
        'Pizza BBQ and Bacon': request.form.get('quantity_BBQ_and_bacon'),
    }

    # Check and add pizzas to order list
    for pizza, quantity in quantities.items():
        if pizza in selected_pizzas and quantity:
            currentOrders.append((pizza, quantity))

    # Process selected drinks in a similar manner
    selected_drinks = request.form.getlist('drinks')
    drink_quantities = {
        'Coca Cola': request.form.get('quantity_Coca_Cola'),
        'Coca Cola Zero': request.form.get('quantity_Coca_Cola_Zero'),
        'Sprite': request.form.get('quantity_Sprite'),
        'Sprite Zero': request.form.get('quantity_Sprite_Zero'),
        'Fuze Tea': request.form.get('quantity_Fuze_tea'),
        'Water': request.form.get('quantity_Water'),
    }

    for drink, quantity in drink_quantities.items():
        if drink in selected_drinks and quantity:
            currentOrders.append((drink, quantity))

    # Retrieve the dine option from session
    dine_option = session.get('dine_option', 'Take away')  # Default to "Take away"

    # Calculate total price here
    total_price = sum(
        (PIZZA_PRICES.get(item, 0) if item in PIZZA_PRICES else DRINK_PRICES.get(item, 0)) * int(qty)
        for item, qty in currentOrders
    )

    # Payment and order details
    payment_method = request.form.get("payment_method")
    rightNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create and store order data
    if currentOrders:
        # Here, the order status is removed from the order tuple
        order_data = (rightNow, order_number, currentOrders, total_price, payment_method, "Waiting", dine_option)
        
        for item in currentOrders:
         print("item",item)
         if "Pizza" in item[0]:
          pizzacounter.append(int(item[1]))
        
        pizzas_per_order_STATUS.append("waiting")
        pizzas_per_order.append(sum(pizzacounter))
        pizzacounter.clear()
        print(pizzas_per_order,pizzas_per_order_STATUS)
        
        # Append to both lists
        data.append(order_data)  # For view_order.html
        datas.append(order_data)  # For order.html

        order_number += 1
        return redirect('/view_order')
    else:
        print("No items selected.")  # Debug print
        return redirect('/create_order')


@app.route('/view_order')
def view_order():
    # Ensure there is at least one order
    if data:
        # Access the latest order
        order = data[-1]

        # Extract order details
        order_time = order[0]
        order_number = order[1]
        order_items = order[2]  # This is a list of tuples (pizza_name, quantity)
        total_price = order[3]

        # Format the order items into a string for display
        items_display = ', '.join([f"{qty} x {pizza}" for pizza, qty in order_items])

        # Only include the latest order in the list to pass to the template
        order_details = [{
            "order_time": order_time,
            "order_number": order_number,
            "items_display": items_display,
            "total_price": total_price
        }]
        print(order[0],order[1],order[2],order[3],order[4],order[5],order[6])
        print(order)
    else:
        # If no orders are present, set order_details to an empty list
        order_details = []

    return render_template('view_order.html', orders=order_details)


@app.route('/current_orders')
@login_required
def show_current_orders():
    filtered_orders = [
        (order[0], order[1], order[2], order[5])  # (date, order_number, order_details, status)
        for order in datas
    ]
    # Debugging print
    print("Filtered Orders:", filtered_orders)
    return render_template('order.html', orders=filtered_orders, preparation=preparation, cooked=cooked)

@app.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    payment_method = request.form.get('payment_method')
    order = data[-1]  # Get the most recent order
    order_number = order[1]
    payment_mode = payment_method  # Set payment_mode

    # Update the payment mode in datas
    for i, order in enumerate(datas):
        if order[1] == order_number:
            datas[i] = order[:4] + (payment_mode,) + order[5:]  # Update payment_mode and remove payment_status
            break

    return redirect('/payment_status')

@app.route('/payment_page')
def payment():
    return render_template('payment_page.html')

@app.route('/payment_status')
@login_required
def payment_status():
    payment_info = []
    for order in datas:
        if len(order) >= 7:  # Ensure there are enough elements
            payment_info.append((order[0], order[1], order[3], order[4], order[6]))  # Correctly access the dine option
        else:
            # Handle the case where order does not have enough elements
            payment_info.append((order[0], order[1], order[3], order[4], 'N/A'))  # Use 'N/A' or some default value

    return render_template("payment_status.html", orders=payment_info)

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    order_number = int(request.form['order_number'])
    item_type = request.form['pizza_type']  
    new_quantity = int(request.form['quantity'])

    # Find the order with the specified order number
    for i, order in enumerate(datas):
        if order[1] == order_number:
            # Update the quantity of the specified item
            order_details = order[2]  # Get the order details
            for j, (item, qty) in enumerate(order_details):
                if item == item_type:
                    # Update the quantity
                    order_details[j] = (item, new_quantity)
                    # Update the order in the datas list
                    datas[i] = (order[0], order[1], order_details, order[3], order[4], order[5])  # Update the full order details
                    break
            break

    return redirect('/current_orders')  # Redirect back to the current orders page

@app.route('/update_payment_status', methods=['POST'])
def update_payment_status():
    # This function will remain but will not update the payment status
    # order_number = int(request.form.get('order_number'))
    # current_payment_status = request.form.get('current_payment_status')

    # Update the payment status in datas (this part is now commented out)
    # for i, order in enumerate(datas):
    #     if order[1] == order_number:
    #         if current_payment_status == 'Not Paid':
    #             # Update payment status to 'Paid'
    #             datas[i] = order[:-2] + ('Paid', order[6])  # Update to 'Paid'
    #         break

    return redirect('/payment_status')




@app.route('/remove_payment_order', methods=['POST'])
def remove_payment_order():
    order_number = int(request.form['order_number'])

    # Remove the order from datas based on the order number
    global datas
    datas = [order for order in datas if order[1] != order_number]

    # Redirect back to the payment status page
    return redirect('/payment_status')

@app.route('/update_pizza_quantity', methods=['POST'])
def update_pizza_quantity():
    global pizzas_per_order, pizzas_per_order_STATUS 
    pizzas_done = request.get_json() #get the value from other python which controls arduino
    print(pizzas_done,pizzas_per_order)
    #logic to math pizzas_done and in which order it is
    while pizzas_done>0:
     print(pizzas_done)
     print ("pizzas_per_order",pizzas_per_order)
     if pizzas_per_order[0]>=pizzas_done:
            
            pizzas_per_order[0]=pizzas_per_order[0]-pizzas_done
            pizzas_done=0
     elif pizzas_per_order[0]<pizzas_done:
              pizzas_done=pizzas_done-pizzas_per_order[0]
              pizzas_per_order[0]=0
 
     # check if the order is fully done
     if pizzas_per_order[0]==0 and pizzas_per_order_STATUS[0]=="preparing":
         used_order = datas[-1]  # replace with actual order number logic
         order_number = used_order[1]
         current_status = used_order[5]
         post_data = {
                'order_number': order_number,
                'current_status': current_status
            }
         
         response = requests.post('http://127.0.0.1:5000/update_order_status', data=post_data)
         print(f"order_number: {order_number}, current_status: {current_status}")
         pizzas_per_order_STATUS.pop(0)
         pizzas_per_order.pop(0)
         print("RESET")

         time.sleep(5)
         return redirect('/current_orders')
    return redirect('/current_orders')
            
     
@app.route('/update_order_status', methods=['POST'])
def update_status():
    global pizzas_per_order_STATUS
    print("UPDATE_STATUS")
    order_number = int(request.form['order_number'])
    current_status = request.form['current_status'].lower()  # Ensuring lowercase match with status_cycle

    print(f"Received Order Number (def Update Status): {order_number}, Current Status: {current_status}")
    
      
    # Define the status cycle
    status_cycle = ["waiting", "preparing", "ready"]

    # Check if we are at the end of the cycle
    if current_status == "ready":
        # Remove the order if status is at the end of the cycle
        global datas
        datas = [order for order in datas if order[1] != order_number]
        return redirect('/current_orders')

    # Find the next status in the cycle
    next_status_index = status_cycle.index(current_status) + 1
    next_status = status_cycle[next_status_index]

    for i, order in enumerate(datas):
        if order[1] == order_number:  # Checking the order_number at index 1
            # Update the order status message in the order tuple
            datas[i] = order[:5] + (next_status,) + order[6:]  # Update to next status
            print(f"Updated Order Status for Order {order_number}: {datas[i]}")
            pizzas_per_order_STATUS[i]=next_status
            break
    
    return redirect('/current_orders')

@app.route('/remove_order', methods=['POST'])
def remove_order():
    order_number = int(request.form['order_number'])

    # Remove from orders
    global datas, preparation, cooked
    datas = [order for order in datas if order[1] != order_number]
    preparation = [order for order in preparation if order[1] != order_number]
    cooked = [order for order in cooked if order[1] != order_number]

    # Redirect back to the order viewing page
    return redirect('/current_orders')

@app.route('/mario_register', methods=['POST'])
def register_order_from_mario():
    data = request.get_json()
    order_time = data['date and time']
    order_number = data['order number']
    order_details = data['order']

    newOrder = (order_time, order_number, order_details)
    datas.append(newOrder)

    return "OK"

@app.route('/luigi_register', methods=['POST'])
def register_order_from_luigi():
    in_preparation = request.get_json()
    order_time = in_preparation['date']
    order_number = in_preparation['order_number']
    order_details = in_preparation['order_details']

    order_in_preparation = (order_time, order_number, order_details)
    preparation.append(order_in_preparation)

    return "OK"

@app.route('/smart_oven_register', methods = ['POST'])
def register_order_from_smart_oven():

    in_cooking = request.get_json()
    order_time = in_cooking['date']
    order_number = in_cooking['order_number']
    order_details = in_cooking['order_details']

    order_in_cooking = (order_time,order_number,order_details)
    cooked.append(order_in_cooking)

    return "OK"

@app.route('/staff_console')
@login_required
def console():
    logged_in_user = session.get('username')  # Retrieve username from session
    return render_template('console.html', logged_in_user=logged_in_user)

@app.route('/staff_login')
def staff_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    global login_chances
    username = request.form.get("username")
    password = request.form.get("password")

    # Debugging output
    print(f"Username: {username}, Password: {password}")

    # Check if the username exists in the users dictionary
    if username in users and bcrypt.check_password_hash(users[username], password):
        session['username'] = username  # Store username in session
        login_chances = 3  # Reset login chances on successful login
        return redirect("/staff_console")  # Redirect to console after successful login
    else:
        login_chances -= 1  # Decrement login chances on each failed attempt

        # If no attempts left, redirect to login page with a reset
        if login_chances <= 0:
            return render_template("error_login.html")

        # Re-render the login page with the updated login_chances
        return render_template("login.html", login_chances=login_chances)

@app.route('/take', methods=['GET'])
def take_one_order():
    if len(datas) == 0:
        return {}

    order = datas[0]
    datas.pop(0)
    (date, orderNumber, order_details) = order

    return {'date': date, 'order_number': orderNumber, 'order_details': order_details}

@app.route('/cook', methods = ['GET'])
def cook_one_order():

    if len(preparation) == 0:
        return {}

    order = preparation[0]
    preparation.pop(0)

    (date, orderNumber,order_details) = order

    return { 'date': date, 'order_number': orderNumber, 'order_details': order_details }

if __name__ == '__main__':
    app.run(debug=True)