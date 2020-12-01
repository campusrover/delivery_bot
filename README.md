# delivery_bot
ROS Delivery Bot

To make the model (including willow garage base with colored boxes as identifiers) load correctly, make sure this repo is located within ../my_ros_data/catkin_ws/src/

To launch modified Gazebo world: roslaunch delivery_bot delivery_world.launch model:=waffle

To navigate/ perform delivery, first: roslaunch delivery_bot delivery_navigation.launch map_file:=/my_ros_data/catkin_ws/src/delivery_bot/map/modified_world.yaml
To deliviver to a single person: python src/deliver_routing.py --mode 2 --name Yifei
To deliver to multiple people: python src/deliver_routing.py --mode 3 --namelist Yifei Pito Daniel