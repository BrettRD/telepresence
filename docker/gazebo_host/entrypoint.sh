#!/bin/bash

# setup ros environment
source /opt/ros/melodic/setup.bash
source /root/catkin_ws/devel/setup.bash

# setup gazebo environment
source "/usr/share/gazebo/setup.sh"

#gzserver --verbose &

# Start virtual X server in the background
# - DISPLAY default is :99, set in dockerfile
# - Users can override with `-e DISPLAY=` in `docker run` command to avoid 
#   running Xvfb and attach their screen
if [[ -x "$(command -v Xvfb)" && "$DISPLAY" == ":99" ]]; then
	echo "Starting Xvfb" 
	Xvfb :99 -screen 0 1600x1200x24+32 &
fi


exec "$@"