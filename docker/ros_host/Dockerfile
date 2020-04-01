FROM ros:melodic-robot

#ROS components
RUN apt-get update && apt-get install -y \
    ros-melodic-joy \
    ros-melodic-turtlesim


#upgrade ffmpeg for aiortc av dependency
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/ffmpeg-4
RUN apt-get update && apt-get upgrade -y

#pip3 and aiortc dependencies
RUN apt-get install -y \
    python3-pip \
    libavdevice-dev \
    libavfilter-dev \
    libopus-dev \
    libvpx-dev \
    libsrtp2-dev \
    pkg-config

#webrtc and other python libs
RUN pip3 install \
    pyyaml \
    aiortc \
    aiohttp \
    rospkg \
    opencv-python \
    websockets


#copy the catkin packages into workspace
WORKDIR /root/catkin_ws/src
COPY ./telepresence ./telepresence

# build packages
WORKDIR /root/catkin_ws
RUN ["/bin/bash", "-c", "source /opt/ros/melodic/setup.bash; catkin_make"]

ADD ./telepresence/docker/ros_host/ros-entrypoint.sh /ros-entrypoint.sh
ENTRYPOINT [ "/ros-entrypoint.sh" ]

