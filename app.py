from flask import Flask, redirect, render_template, request, session, send_file
import sqlite3
import base64
import io
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image

from helpers import login_required

app = Flask(__name__)
app.secret_key="__privatekey__"

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/index.html')
@login_required
def index_pravi():
    return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        connection = sqlite3.connect('databases.db')
        cursor = connection.cursor()
        
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        surname = request.form.get("surname")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        confirmation = request.form.get("confirmation")

        if not email:
            print("Email is required")
            return render_template("error.html")
        elif not password:
            print("Password is required")
            return render_template("error.html")
        elif not name:
            print("Name is required")
            return render_template("error.html")
        elif not surname:
            print("Surname is required")
            return render_template("error.html")
        elif not confirmation:
            print("Confirmation is required")
            return render_template("error.html")
        if password != confirmation:
            print("Password do not match")
            return render_template("error.html")

        hash = generate_password_hash(password)

        statement = f"SELECT * FROM users WHERE email='{email}' AND password='{hash}'"
        cursor.execute(statement)
        new_user = cursor.fetchone()
        if new_user:
            return render_template("error.html")
        else:
            if new_user:
                cursor.execute("INSERT INTO users (name, surname, email, password, day_birth, month_birth, year_birth, starting_money) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, email, hash, day, month, year, 100000))

                session["user_id"] = new_user[0]

                connection.commit()
                connection.close()
            return redirect("/")
    else:
        return render_template('register.html')    


@app.route('/login', methods=['GET', 'POST'])
def login():

    session.clear()

    if request.method == 'POST':
        connection = sqlite3.connect('databases.db')
        cursor = connection.cursor()

        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            print("Email is required")
            return render_template("error.html")
        elif not password:
            print("Password is required")
            return render_template("error.html")
        
        statement = f"SELECT * FROM users WHERE email = '{email}'"
        cursor.execute(statement)
        check = cursor.fetchone()
        if not check or check_password_hash((check[4]), password) == False:
            return render_template("login.html")

        session["user_id"] = check[0]

        connection.commit()
        connection.close()

        return redirect("/")
    else:      
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    user_id = session["user_id"]
    
    
    if request.method == "POST":
        connection = sqlite3.connect('databases.db')
        cursor = connection.cursor()

        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))

        print(product_id)
        # get the current cash of the user
        starting_money = f"SELECT starting_money FROM users WHERE id = {user_id}"
        cursor.execute(starting_money)
        cash = cursor.fetchone()[0]


        # get the item price and if its in stock
        statement = f"SELECT * FROM watches WHERE id = {product_id}"
        cursor.execute(statement)
        item_properties = cursor.fetchone()

        # for price
        item_price = int(item_properties[8])
        # for stock
        item_stock = item_properties[9]
        

        # total money user has to pay
        total = item_price * quantity
        print(item_price, item_stock, quantity, cash, total)
        # if statements
        if (cash < total) or (item_stock < quantity):
            return render_template("error.html")
        else:
            cursor.execute("UPDATE users SET starting_money = ? WHERE id = ?", (cash - total, user_id))
            cursor.execute("INSERT INTO transactions (user_id, watch_id, amount, price, type, total_price) VALUES (?, ?, ?, ?, ?, ?)", (user_id, product_id, quantity, item_price, 'buy', total))
            connection.commit()
            connection.close()

        return render_template('shopping_cart.html')
    else:
        return render_template('shopping_cart.html')

@app.route('/shopping_cart.html')
def shopping_cart2():
    return redirect('/shopping_cart')

@app.route('/account.html')
def account():
    return render_template('account.html')

@app.route('/login.html')
def login2():
    return redirect('/login')

@app.route('/register.html')
def register2():
    return redirect('/register')

@app.route('/onama.html')
@login_required
def onama():
    return render_template('onama.html')

@app.route('/brendovi.html')
@login_required
def brendovi():
    return render_template('brendovi.html')

@app.route('/kontakt.html')
@login_required
def kontakt():
    return render_template('kontakt.html')

@app.route('/casio.html')
@login_required
def casio():
    return render_template('casio.html')

@app.route('/citizen.html')
@login_required
def citizen():
    return render_template('citizen.html')

@app.route('/diesel.html')
@login_required
def diesel():
    return render_template('diesel.html')

@app.route('/festina.html')
@login_required
def festina():
    return render_template('festina.html')

@app.route('/fossil.html')
@login_required
def fossil():
    return render_template('fossil.html')

@app.route('/klein.html')
@login_required
def klein():
    return render_template('klein.html')

@app.route('/roamer.html')
@login_required
def roamer():
    return render_template('roamer.html')

@app.route('/rolex.html')
@login_required
def rolex():
    connection = sqlite3.connect('databases.db')
    cursor = connection.cursor()

    statement = f"SELECT * FROM watches WHERE brand = 'ROLEX'"
    cursor.execute(statement)
    rolex = cursor.fetchall()

    return render_template('rolex.html', rolex = rolex)
    
@app.route('/seiko.html')
@login_required
def seiko():
    return render_template('seiko.html')

@app.route('/swatch.html')
@login_required
def swatch():
    return render_template('swatch.html')

@app.route('/tissot.html')
@login_required
def tissot():
    return render_template('tissot.html')

@app.route('/zenith.html')
@login_required
def zenith():
    return render_template('zenith.html')

if __name__ == "__main__":
    app.run(debug=True)   
