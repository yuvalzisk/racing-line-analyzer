FROM ros:jazzy-ros-base

# Install Python plotting dependencies
RUN apt-get update && apt-get install -y \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# Create project workspace
WORKDIR /app

# Copy ROS 2 source code
COPY racing_ws/src /app/racing_ws/src

# Build the ROS 2 package
WORKDIR /app/racing_ws

RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && \
    colcon build --packages-select racing_line_analyzer"

# Default working directory
WORKDIR /app
