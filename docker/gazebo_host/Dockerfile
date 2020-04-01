FROM gazebo:libgazebo9-bionic


##### set up gazebo web

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -q -y \
    curl
#get nodejs 12 package lists
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -

# install packages
RUN apt-get update && apt-get install -q -y \
    build-essential \
    cmake \
    imagemagick \
    libboost-all-dev \
    libgts-dev \
    libjansson-dev \
    libtinyxml-dev \
    mercurial \
    nodejs \
    pkg-config \
    psmisc \
    xvfb
#    nodejs-legacy \
#    npm \

# clone gzweb
ENV GZWEB_WS /root/gzweb
WORKDIR $GZWEB_WS
#RUN hg clone https://bitbucket.org/osrf/gzweb $GZWEB_WS
COPY ./telepresence/docker/gazebo_host/gzweb $GZWEB_WS


# build gzweb
#RUN hg up gzweb_1.4.0 \
RUN hg up default \
    && xvfb-run -s "-screen 0 1280x1024x24" ./deploy.sh -m -t

# setup environment
EXPOSE 8080
EXPOSE 7681





##### setup ROS

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

# install ros packages
ENV ROS_DISTRO melodic


#install ros-melodic-desktop
RUN apt-get update && apt-get install -y \
    ros-melodic-desktop \
    && rm -rf /var/lib/apt/lists/*



##### set up workspace 

# build packages
WORKDIR /root/catkin_ws
RUN ["/bin/bash", "-c", "source /opt/ros/melodic/setup.bash; catkin_make"]

#add entrypoint
ADD ./telepresence/docker/gazebo_host/entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

WORKDIR $GZWEB_WS
#CMD gzserver --verbose & npm start
