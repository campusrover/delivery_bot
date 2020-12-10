#!/usr/bin/env python

import sqlite3

conn = sqlite3.connect('database.db')


# create table
conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER primary key, recipient_id int, status text, create_time datetime default current_timestamp, robot_id int)')
conn.commit()
conn.execute('CREATE TABLE IF NOT EXISTS robots (id INTEGER primary key, status text, update_time datetime default current_timestamp)')
conn.commit()
conn.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER primary key, name text, location_x real, location_y real )')
conn.commit()


# clear old data
conn.execute("delete from employees")
conn.commit()
conn.execute("delete from robots")
conn.commit()
conn.execute("delete from tasks")
conn.commit()


# initialize robot data
conn.execute("insert into robots (id, status) values(1, 'idle')")
conn.commit()
conn.execute("insert into robots (id, status) values(2, 'idle')")
conn.commit()


# initialize employee data
conn.execute("insert into employees values(1, 'Pito', -3.37, -10.42)")
conn.commit()
conn.execute("insert into employees values(2, 'Daniel', 0.08, -10.1)")
conn.commit()
conn.execute("insert into employees values(3, 'Yifei', -6.15, -10.42)")
conn.commit()


# add initial two tasks
conn.execute("insert into tasks(recipient_id, status, robot_id) values(1, 'new_task', 1)")
conn.commit()
conn.execute("insert into tasks(recipient_id, status, robot_id) values(2, 'new_task', 1)")
conn.commit()
conn.execute("insert into tasks(recipient_id, status, robot_id) values(3, 'new_task', 2)")
conn.commit()