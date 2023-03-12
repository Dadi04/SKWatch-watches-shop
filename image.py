import sqlite3

conn = sqlite3.connect('databases.db')
cursor = conn.cursor()

with open('static/images/citizen1.png', 'rb') as f:
    data=f.read()

cursor.execute("UPDATE watches SET image = ? WHERE id = 9", (data,))


conn.commit()
cursor.close()
conn.close()