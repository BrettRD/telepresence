# Telepresence
Telepresence by means of ROS, webrtc, some python, and a lot of Docker.

This is a ros package that hopes to be turnkey on host machines without ROS.

This package forwards joystick input over WebRTC, and maps it to a turtlesim node for output.\
The WebRTC video feed is only partly built, and the audio is going to take some doing.

## Installation:
Get Docker,\
Get ROS, and set up a workspace. (dependency to be removed soon)\
Pull this repo into a ROS Catkin workspace. (This package has no output without ROS on the host machine.)\
Get the ROS turtlesim node.

Whatever is in the docker containers will run without errors regardless of what's on the host.\
I'd like to get X11 forwarding from the container to the host to remove the need for native ROS.

## Docker:
Head into `telepresence/docker/` and run `docker-compose up --build`\
Then run `source join-ros.sh` to get your native ROS to refer to the roscore running in docker.\
To see the turtlebot, run on the host `rosrun turtlesim turtlesim_node`\

## Future work:
- WebRTC signalling server in a docker container
- Javascript client for control and video, also in Docker
- WebRTC stream <-> ROS image topic
- WebRTC stream <-> ROS audio topic
- Examples of this running on robots made of zip ties and milk crates.

## Known issues:
### ROS on the host dependency 
ROS on the host is only used for running a single node that interacts with the Desktop environment.\
Patches that either enable X11 forwarding, or provide more interesting interaction are vey welcome.

### Chatroom collisions:
This uses AppRTC for the WebRTC signalling server, and doesn't close the connection nicely.\
If the chatroom name has been used in the last 24hrs, the WebRTC nodes will crash.\
Start a new chatroom by changing the string in `telepresence/docker/.env'\
Ideally this would move to a different signalling server which has a separate docker container.

### Hardcoded Joystick name:
The docker-compose.yml refers to `/dev/input/js0`, and will complain bitterly if it doesn't exist.\
Patches welcome to support alternative input devices.\
Ultimately, control will be via a browser anyway

