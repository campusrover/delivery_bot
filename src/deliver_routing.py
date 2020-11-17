#!/usr/bin/env python

# navigation for delivery bot - must launch Action server using delivery_navigation.launch first

import rospy
import actionlib
import sys, argparse
import pickle
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

parser = argparse.ArgumentParser(description='Delivery Routing')
parser.add_argument('--name', type=str, default="Pito",
                    help='Enter the name of the person accepting delivery')
args = parser.parse_args()

jar_opener_1 = open('name_color_dict.pickle','rb')
name_color_dict = pickle.load(jar_opener_1)
jar_opener_1.close()
jar_opener_2 = open('color_location_dict.pickle','rb')
color_location_dict = pickle.load(jar_opener_2)
jar_opener_2.close()

#name_color_dict = {"Pito":"Red", "Daniel":"Green", "Yifei":"Blue"}
#color_location_dict = {"Red":[-3.37, -10.42], "Blue":[0.92, -10.42], "Green":[-6.15, -10.42]}

def movebase_client(color_input):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = color_location_dict[color_input][0]
    goal.target_pose.pose.position.y = color_location_dict[color_input][1]
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        print("Name Input: ", args.name)
        print("Identity color: ", name_color_dict[args.name])
        result = movebase_client(name_color_dict[args.name])
        if result:
            rospy.loginfo("Goal reached!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation terminated.")