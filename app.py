from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)
app.secret_key="__privatekey__"

@app.route('/')
def index():
    return render_template('index.html')

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

        statement = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
        cursor.execute(statement)
        data = cursor.fetchone()
        if data:
            return render_template("error.html")
        else:
            if not data:
                cursor.execute("INSERT INTO users (name, surname, email, password, day_birth, month_birth, year_birth, starting_money) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, email, password, day, month, year, 100000))
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
        
        statement = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
        cursor.execute(statement)
        if not cursor.fetchone():
            return render_template("login.html")
        else:
            return redirect("/")
    else:      
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)   
