#!/usr/bin/env python

from flask import Flask, request, Response, g, jsonify
import sqlite3
import json

import rospy
from std_msgs.msg import String

app = Flask(__name__)

conn = sqlite3.connect('database.db')
@app.route('/')
def backend_entrance():
    robot_status = g.db.execute("select * from robots where status='idle'").fetchall()
    if len(robot_status) > 0:
        return jsonify(
            available = True
        )
    else:
        return jsonify(
        available = False
        )

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

    employee_find = g.db.execute("select * from employees where name='{}' COLLATE NOCASE".format(deliver_data["name"])).fetchall()
    if(len(employee_find) == 0):
        return jsonify(
            findEmployee = False
        )

    selected_robot = g.db.execute("select id from robots where status='idle' order by random() limit 1").fetchall()[0][0]
    g.db.execute("INSERT INTO tasks (recipient_id, status, robot_id) VALUES(?, ?, ?)", (employee_find[0][0], 'new_task', selected_robot))
    g.db.commit()
    return jsonify(
            findEmployee = True
        )


if __name__ == '__main__':
    app.run(debug=True)