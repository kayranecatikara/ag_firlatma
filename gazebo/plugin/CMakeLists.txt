cmake_minimum_required(VERSION 3.16)
project(ag_fizik)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

find_package(gz-cmake3 REQUIRED)
find_package(gz-plugin2 REQUIRED COMPONENTS register)
find_package(gz-sim8 REQUIRED)
find_package(gz-math7 REQUIRED)
find_package(gz-common5 REQUIRED)
find_package(sdformat14 REQUIRED)
find_package(gz-transport13 REQUIRED)
find_package(gz-msgs10 REQUIRED)

add_library(AgFizik SHARED AgFizik.cc)
target_link_libraries(AgFizik
  PRIVATE gz-plugin2::register
  PRIVATE gz-sim8::gz-sim8
  PRIVATE gz-math7::gz-math7
  PRIVATE gz-common5::gz-common5
  PRIVATE sdformat14::sdformat14
  PRIVATE gz-transport13::gz-transport13
  PRIVATE gz-msgs10::gz-msgs10)
