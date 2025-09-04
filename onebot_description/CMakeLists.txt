cmake_minimum_required(VERSION 3.11 FATAL_ERROR)

#Project Name
project(
  onebot_description
  VERSION 1.0
  LANGUAGES CXX
)

# —— Include guards ——
if (PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      "In-source builds not allowed. Please make a new directory(called a build directory) and run CMake from there."
  )
endif()

# —— Add dependencies via CPM ———

find_package(ament_cmake REQUIRED)

message(STATUS "version: ${PROJECT_VERSION}")

add_subdirectory(examples)

string(TOLOWER ${PROJECT_NAME}/version.h VERSION_HEADER_LOCATION)

install(
  DIRECTORY config launch meshes urdf rviz
  DESTINATION share/${PROJECT_NAME}
  )
ament_package()
