
#!/usr/bin/env python
import rospy
import sys, argparse
import math
import time
import tf
import cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry

# this script is used to verify if the person is present or not - green box: the person is present, deliver; red box: the person is not in office, do not deliver
img = []
green_box_indicator = False

# define bridge for OpenCV conversion
bridge = cv_bridge.CvBridge()

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

rospy.init_node('cube_detector')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, image_callback) 

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


# set rate
rate = rospy.Rate(5)
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()

detect_status()
