#!/bin/bash
source ~/catkin_ws/devel/setup.bash
cd ~/catkin_ws/src/delivery_bot/ && ./ngrok http 5000
