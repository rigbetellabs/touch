cmake_minimum_required(VERSION 3.0.2)
project(touch)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  rviz_visual_tools
)
catkin_package(
  LIBRARIES
  INCLUDE_DIRS
  CATKIN_DEPENDS
  DEPENDS
    EIGEN3
)
include_directories(SYSTEM ${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIR} ${EIGEN3_INCLUDE_DIRS})

add_executable(create_rectangle src/rectangle.cpp)
target_link_libraries(create_rectangle ${catkin_LIBRARIES} ${Boost_LIBRARIES})
install(TARGETS create_rectangle DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})