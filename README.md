# delivery_bot
author1 -- Yifei Han (yifeih@brandeis.edu)
author2 -- Daniel Zhang (danielzhang@brandeis.edu)

## Video Link



## Project Introduction
This is the multi-robot indoor delivery system to help solve the problem of delivery. Recipient or delivery person may wait each other for a long time or miss each other, which is a waste of time and resources. With this indoor delivery robot. delivery person can simply put food in the box of the robot and commnicate who should it send to using human voice. 

technically. it used Alexa as front-end. Alexa will receive human command to record who shuold deliver to. it will firstly check whether there is an employee with the specified name working in the building. if there is. it will store the task. otherwise it will ask the person to make sure the name is correct. 

once the task stored. there is a node which resposible to decide wether the robot shuold start to deliver. the setting is that robot will wait at the reception for about 5 minutes, then start to deliver if there is food inside the box.

For the delivery part, gmapping is used to build the map for the building first which make it much faster to find the shortest path to deliver the food. it will not do random wandering any more.

To find the shortest path, AMCL algorithm is used to fidn thr shortest path using estimation based on current location(which is comparision from the Lidar data and data from gmapping service). then it used bfs and dfs to find the shortest path and deliver the food.

During delivery process. OpenCv is also sed to detect wheter recipient is in office or not. if there is a green light, it means recipient is in office. it will deliver it there. otherwise it will deliver again at the second round. if recipient is still not in office(detect red light using camera data and openCV). robot will deliver it to the reception desk and back to the door.


## How to start
To make the model (including willow garage base with colored boxes as identifiers) load correctly, make sure this repo is located within ../my_ros_data/catkin_ws/src/

To launch modified Gazebo world: roslaunch delivery_bot delivery_world.launch model:=waffle

To navigate/ perform delivery, first: roslaunch delivery_bot delivery_navigation.launch map_file:=/my_ros_data/catkin_ws/src/delivery_bot/map/modified_world.yaml
To deliviver to a single person: python src/deliver_routing.py --mode 2 --name Yifei
To deliver to multiple people: python src/deliver_routing.py --mode 3 --namelist Yifei Pito Daniel


