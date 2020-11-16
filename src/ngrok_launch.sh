#!/bin/bash
apt-get install sqlite3
source ~/catkin_ws/devel/setup.bash
cd ~/catkin_ws/src/delivery_bot/ && ./ngrok http -subdomain=deliverybot 5000
