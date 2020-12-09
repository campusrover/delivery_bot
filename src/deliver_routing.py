#!/usr/bin/env python

# navigation for delivery bot - must launch Action server using delivery_navigation.launch first

import rospy
import actionlib
import sys, argparse
import pickle
import time
import cv2, cv_bridge, numpy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from datetime import datetime
import sqlite3

conn = sqlite3.connect('database.db')

parser = argparse.ArgumentParser(description='Delivery Routing')
parser.add_argument('--mode', type=int, default='1', help='1 - delivery, 2 - delivery and check if person is present, 3 - delivery multiple with check')
parser.add_argument('--namelist', nargs='+', default=[])
parser.add_argument('--name', type=str, default="Pito",
                    help='Enter the name of the person accepting delivery')
args = parser.parse_args()

# jar_opener = open('name_location_dict.pickle','rb')
# name_color_dict = pickle.load(jar_opener_1)
# jar_opener.close()

rospy.init_node('deliver_routing')

img = []
delivery_queue = []
delivery_2nd_attempt = []
green_box_indicator = False

# define bridge for OpenCV conversion
bridge = cv_bridge.CvBridge()

def print_queue_status():
    global delivery_queue
    global delivery_2nd_attempt
    print ("Delivery Queue: ", delivery_queue)
    print ("Delivery 2nd: ", delivery_2nd_attempt)

def movebase_client(name_input, x, y):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = -1

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def image_callback(msg):
    global img
    global green_box_indicator

    cv_image = bridge.imgmsg_to_cv2(msg) #convert img to OpenCV type
    img = cv_image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV Image", hsv)
    cv2.waitKey(10)
    lower_green = numpy.array([ 50, 0, 0])
    upper_green = numpy.array([ 75, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green) 
    masked = cv2.bitwise_and(img, img, mask=mask) 
    cv2.imshow("masked Image", masked)
    cv2.waitKey(10)
    M = cv2.moments(mask)
    if M['m00'] > 0:
        green_box_indicator = True
    else:
        green_box_indicator = False

def rotate_check():
    global green_box_indicator
    if green_box_indicator:
        return True
    t = Twist()
    t.linear.x = 0
    t.angular.z = 0.5
    pub.publish(t)
    t_end = time.time() + 5
    while time.time() < t_end:
        if green_box_indicator:
            t.angular.z = 0
            pub.publish(t)
            return True
    t.angular.z = 0
    pub.publish(t)
    return False


def detect_status():
    global green_box_indicator
    # return true if green detected (meaning the person is present)
    # call rotate check to rotate the robot - return false if still no green 
    if green_box_indicator:
        return True
    else:
        return rotate_check()

def deliver_n_check(name_input):
    # head to location based on name, check if person there by looking for green box
    global conn
    coordinate = conn.execute("select employees.location_x, employees.location_y from employees join tasks on tasks.recipient_id=employees.id where employees.id=? ", (name_input, )).fetchall()[0]
    movebase_client(name_input, coordinate[0], coordinate[1])
    return detect_status()

def multiple_delivery():
    global delivery_queue
    global delivery_2nd_attempt
    global conn

    while len(delivery_queue) > 0:
        print_queue_status()
        k = delivery_queue.pop(0)
        if not deliver_n_check(k):
            print("NOT delivered, will try again!")
            delivery_2nd_attempt.append(k)
        else:

            conn.execute("update tasks set status='completed' where id=? ", (k, ))
            conn.commit()

            print("Delivered!")
    while len(delivery_2nd_attempt) > 0:
        print_queue_status()
        k = delivery_2nd_attempt.pop(0)
        if not deliver_n_check(k):
            print("Cannot deliver to ", k)
        else:

            conn.execute("update tasks set status='completed' where id=? ", (k, ))
            conn.commit()
            
            print("Delivered (2 nd)")

    movebase_client(name_input, 0, 0)

pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, image_callback) 


if __name__ == '__main__':
    if args.mode != 3: 
        try:
            print("Name Input: ", args.name)
            if args.mode == 2:
                result = deliver_n_check(args.name)
                if result:
                    print("the person is there!")
                    rospy.loginfo("Goal reached and the person is there!")
            else:
                result = movebase_client(args.name)
                if result:
                    print("Delivered!")
                    rospy.loginfo("Goal reached!")
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation terminated.")
    else: # multiple delivery, queue mode 
        try:
            print("Name List Input: ", args.namelist)
            delivery_queue = args.namelist
            multiple_delivery()
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation terminated.")