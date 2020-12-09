import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('CREATE TABLE IF NOT EXISTS tasks (recipient_id int, status text, create_time datetime default current_timestamp, robot_id int)')
conn.commit()
conn.execute('CREATE TABLE IF NOT EXISTS robots (id int primary key, status text, update_time datetime default current_timestamp)')
conn.commit()
conn.execute('CREATE TABLE IF NOT EXISTS employees (id int primary key, name text, location_x real, location_y real )')
conn.commit()

conn.execute("insert into employees values(1, 'Pito', -3.37, -10.42)")
conn.commit()

conn.execute("insert into employees values(1, 'Pito', -3.37, -10.42)")
conn.commit()
conn.execute("insert into employees values(2, 'Daniel', 0.08, -10.1)")
conn.commit()
conn.execute("insert into employees values(3, 'Pito', -6.15, -10.42)")
conn.commit()
