LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS) 

# give module name
LOCAL_MODULE := hdb 

# list your C files to compile
LOCAL_SRC_FILES := hdb.c

# this option will build executables instead of building library for android application.
include $(BUILD_EXECUTABLE)
