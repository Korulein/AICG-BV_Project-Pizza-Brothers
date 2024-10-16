from flask import Flask, render_template,request, redirect

app = Flask(__name__)
currentOrders = []

@app.route('/')
def welcome():
    return render_template("hello.html")
    
@app.route('/cash_register')
def cash_register():
    return render_template("mario.html")

@app.route('/register_order', methods = ['POST'] )
def register_order():
    pizza = request.form.getlist('pizza')
    currentOrders.append(pizza)
    print("Registered Pizza")
    print(pizza)

    return redirect('/cash_register')

@app.route('/current_orders')
def show_current_orders():        
    return render_template('order.html',
                           currentOrders=currentOrders)


if __name__ == '__main__':  
    app.run(debug=True)


# py -m flask run -p 5000