FROM osrf/ros:noetic-desktop-full

RUN apt-get update && apt-get install -y \
    python3-pip \
    ros-noetic-cv-bridge \
    ros-noetic-image-transport \
    git

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc