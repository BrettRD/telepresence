FROM ros:melodic-robot


#upgrade ffmpeg for aiortc av dependency
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/ffmpeg-4
RUN apt-get update && apt-get upgrade -y

#ROS components
RUN apt-get install -y \
    ros-melodic-ros-control \
    ros-melodic-ros-controllers \
    ros-melodic-joy

#aiortc dependencies
RUN apt-get install -y \
    libavdevice-dev \
    libavfilter-dev \
    libopus-dev \
    libvpx-dev \
    libsrtp2-dev \
    pkg-config

#python3
RUN apt-get install -y \
    python3-pip

#webrtc and other python libs
RUN pip3 install \
    pyyaml \
    aiortc \
    aiohttp \
    rospkg \
    opencv-python \
    websockets



VOLUME /root/.ros
VOLUME /root/config

# ethernet/ip control ports
#EXPOSE 2222/udp
#EXPOSE 44818

#copy the catkin packages into workspace
WORKDIR /root/catkin_ws/src
COPY ./telepresence ./telepresence
COPY ./turtlebot ./turtlebot


# build packages
WORKDIR /root/catkin_ws
RUN ["/bin/bash", "-c", "source /opt/ros/melodic/setup.bash; catkin_make"]

ADD ./telepresence/docker/ros_host/ros-entrypoint.sh /ros-entrypoint.sh
ENTRYPOINT [ "/ros-entrypoint.sh" ]

