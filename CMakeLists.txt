cmake_minimum_required(VERSION 3.5)
Project("SDFGen")

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries

# SET(CMAKE_BUILD_TYPE Coverage)
SET(CMAKE_BUILD_TYPE Release)

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)

#These flags might not work on every system, especially the release flags, comment out as needed
set(CMAKE_CXX_FLAGS "-O3")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g")

message(STATUS "CMAKE_SYSTEM_PROCESSOR: " ${CMAKE_SYSTEM_PROCESSOR})
message(STATUS "CMAKE_OSX_ARCHITECTURES: " ${CMAKE_OSX_ARCHITECTURES})

# Determine target architecture (use CMAKE_OSX_ARCHITECTURES for macOS cross-compilation)
IF(CMAKE_OSX_ARCHITECTURES)
    SET(TARGET_ARCH ${CMAKE_OSX_ARCHITECTURES})
ELSE()
    SET(TARGET_ARCH ${CMAKE_SYSTEM_PROCESSOR})
ENDIF()

message(STATUS "TARGET_ARCH: " ${TARGET_ARCH})

IF(${TARGET_ARCH} MATCHES "x86_64")
    IF("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
        set(CMAKE_CXX_FLAGS_RELEASE "-O3")
    ELSE()
        set(CMAKE_CXX_FLAGS_RELEASE "-O3 -msse4.2 -mfpmath=sse -mtune=native")
    ENDIF()
ELSEIF((${TARGET_ARCH} MATCHES "aarch64") OR (${TARGET_ARCH} MATCHES "arm64"))
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
ELSE()
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
ENDIF()

add_executable(${PROJECT_NAME}
  SDFGen/main.cpp  SDFGen/makelevelset3.cpp SDFGen/array1.h  SDFGen/array2.h  SDFGen/array3.h  SDFGen/hashgrid.h  SDFGen/hashtable.h SDFGen/makelevelset3.h  SDFGen/util.h  SDFGen/vec.h
  )

install(TARGETS ${PROJECT_NAME} DESTINATION pysdfgen)
