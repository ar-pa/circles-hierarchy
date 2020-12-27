cmake_minimum_required(VERSION 3.15)
project(circles-hierarchy)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2")

add_executable(circles-hierarchy-core src/main.cpp)