FROM ros:melodic-robot

RUN apt-get update

RUN apt-get install -y \
    ros-melodic-ros-control \
    ros-melodic-ros-controllers \
    ros-melodic-joy

VOLUME /root/.ros
VOLUME /root/config

# ethernet/ip control ports
#EXPOSE 2222/udp
#EXPOSE 44818

#copy the catkin packages into workspace
WORKDIR /root/catkin_ws/src
COPY ./diggy ./diggy
COPY ./turtlebot ./turtlebot


# build packages
WORKDIR /root/catkin_ws
RUN ["/bin/bash", "-c", "source /opt/ros/melodic/setup.bash; catkin_make"]

ADD ./diggy/docker/ros_host/ros-entrypoint.sh /ros-entrypoint.sh
ENTRYPOINT [ "/ros-entrypoint.sh" ]

