# This file handles building each task as sub-project.
#
# Each task becomes an independent project in which you can experiment.
#
# Tasks are added as separate sub-projects so as compilation errors in
# one task don't affect another task.

cmake_minimum_required(VERSION 3.30)
project(aoc)

set(CMAKE_CXX_STANDARD 23)


# Add tasks subprojects
#include(cmake/utils.cmake)
add_subdirectory(day-01)
add_subdirectory(day-02)
