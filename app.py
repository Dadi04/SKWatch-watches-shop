from flask import Flask, redirect, render_template, request
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash
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
        if cursor.fetchone():
            return render_template("error.html")
        else:
            if not cursor.fetchone():
                cursor.execute("INSERT INTO users (name, surname, email, password, day_birth, month_birth, year_birth, starting_money) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, email, hash, day, month, year, 100000))
                connection.commit()
                connection.close()
            return redirect("/")
    else:
        return render_template('register.html')    


@app.route('/login', methods=['GET', 'POST'])
def login():
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
        if not cursor.fetchone() or not check_password_hash(statement[0]["hash"], password):
            return render_template("login.html")
        else:
            return redirect("/")
    else:      
        return render_template('login.html')

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
    return render_template('rolex.html')

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
