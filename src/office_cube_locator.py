
#!/usr/bin/env python
import rospy
import sys, argparse
import math
import tf
import cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry

# this script is used to verify if the person is present or not - green box: the person is present, deliver; red box: the person is not in office, do not deliver

# define bridge for OpenCV conversion
bridge = cv_bridge.CvBridge()
movement_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

#TODO: implementation