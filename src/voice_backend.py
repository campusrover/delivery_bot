from flask import Flask, request, Response, g
import rospy
from std_msgs.msg import String
import sqlite3
import json

app = Flask(__name__)

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS tasks (recipient text, phone text, status text, create_time datetime default current_timestamp)')

@app.route('/')
def backend_entrance():
    return Response(status=200)

@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/deliver', methods=['GET', 'POST'])
def deliver():
    deliver_data = request.get_json(force=True)
    g.db.execute("INSERT INTO tasks (recipient, phone, status) VALUES(?, ?, ?)", (deliver_data["name"], deliver_data["phone"], 'new_task'))
    g.db.commit()
    return "received"

if __name__ == '__main__':
    app.run()