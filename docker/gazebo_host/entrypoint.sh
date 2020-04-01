#!/bin/bash

# setup ros environment
source /opt/ros/melodic/setup.bash
source /root/catkin_ws/devel/setup.bash

# setup gazebo environment
source "/usr/share/gazebo/setup.sh"

gzserver --verbose & npm start

exec "$@"