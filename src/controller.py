
import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect('database.db')


if __name__ == '__main__':
    while(True):

        robot_status = conn.execute("select status, update_time as '[timestamp]' from robots where id=1").fetchall()[0]
        tasks = conn.execute("select recipient from tasks where robot_id=1 and status='new_task'").fetchall()[0]
        print(tasks)
        last_modify_time = datetime.strptime(robot_status[1], '%Y-%m-%d %H:%M:%S')
        time_diff =(datetime.now() - last_modify_time).total_seconds() / 60.0
        if robot_status[0] != "idle" or time_diff > 5 or len(tasks) == 0:
            pass
        task_param = ""
        for task in tasks:
            task_param  = task_param + " " + task
       
        conn.execute("update robots set status='working' where id=1")
        conn.commit()

        os.system("python {}/deliver_routing.py --mode 3 --namelist {}".format(os.getcwd(), task_param))  

