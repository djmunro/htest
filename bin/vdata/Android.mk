LOCAL_PATH := $(call my-dir)
INCLUDE_PATH := gmplatform/pal

include $(CLEAR_VARS)
LOCAL_MODULE := pal-integration-vdata
LOCAL_MODULE_TAGS := tests
LOCAL_CFLAGS += -g -Wall -Werror -std=gnu++11 -Wno-missing-field-initializers
LOCAL_SHARED_LIBRARIES += libgmpal
LOCAL_C_INCLUDES := $(LOCAL_PATH)/../inc \
                    $(LOCAL_PATH)/../src/framework/ipcLib/inc \
                    $(LOCAL_PATH)/../src/framework/vdatalib/inc \
                    $(LOCAL_PATH)/../src/powermoding
                        
LOCAL_C_INCLUDES += \
    $(INCLUDE_PATH) \
    $(INCLUDE_PATH)/vdata \
    $(INCLUDE_PATH)/vdata/pal \
    $(INCLUDE_PATH)/powermoding \
    $(INCLUDE_PATH)/powermoding/pal \
    $(LOCAL_PATH)/src/framework/communicator/inc 

LOCAL_SRC_FILES := vdata_tests.cpp

include $(BUILD_NATIVE_TEST)
