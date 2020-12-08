import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect('database.db')

def check_run_robot(id):
        robot_status = conn.execute("select status, update_time as '[timestamp]' from robots where id={}".format(id)).fetchall()[0]
        tasks = conn.execute("select recipient from tasks where robot_id={} and status='new_task'".format(id)).fetchall()

        print(tasks)
        print(robot_status)

        last_modify_time = datetime.strptime(robot_status[1], '%Y-%m-%d %H:%M:%S')
        time_diff =(datetime.now() - last_modify_time).total_seconds() / 60.0
        if robot_status[0] != "idle" or time_diff < 5 or len(tasks) == 0:
            return
        task_param = ""
        for task in tasks:
            task_param  = task_param + " " + task[0]
       
        conn.execute("update robots set status='working' where id={}".format(id))
        conn.commit()

        os.system("python {}/deliver_routing.py --mode 3 --namelist {}".format(os.getcwd(), task_param))  



if __name__ == '__main__':
    
    while(True):
        check_run_robot(1)
        check_run_robot(2)