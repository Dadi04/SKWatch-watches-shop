from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('databases.sql')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM users WHERE name = '"+name+"' AND passoword = '"+password+"'"
        cursor.execute(query)

        results = cursor.fetchall()

        if len(results) == 0:
            print("Sorry Incorrect Credentials Provided.")
        else: 
            return render_template("")
        
    return render_template('login.html')