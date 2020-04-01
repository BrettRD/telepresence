FROM gazebo:libgazebo9-bionic




##### setup ROS


# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros1-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools 

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV ROS_DISTRO melodic
# bootstrap rosdep
RUN rosdep init && \
  rosdep update --rosdistro $ROS_DISTRO


#install ros
RUN apt-get install -y \
    ros-melodic-robot \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update &&  apt-get install -y \
    ros-melodic-gazebo-ros \
    && rm -rf /var/lib/apt/lists/*


##### set up workspace 
#copy the catkin packages into workspace
WORKDIR /root/catkin_ws/src
RUN git clone https://github.com/ros-simulation/gazebo_ros_demos.git
COPY ./telepresence ./telepresence

# build packages
WORKDIR /root/catkin_ws
RUN ["/bin/bash", "-c", "source /opt/ros/melodic/setup.bash; catkin_make"]

#add entrypoint
ADD ./telepresence/docker/gazebo_host/entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
