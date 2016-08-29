#include <gtest/gtest.h>
#include <algorithm>
#include <mutex>
#include <condition_variable>
#include <unistd.h>

#include "pal_vehicle_camera.h"
#include "pal_vehicle_customization.h"
#include "pal_vehicle_dateandtime.h"
#include "pal_vehicle_audio.h"
#include "pal_vehicle_fuel.h"
#include "pal_vehicle_cruisecontrol.h"
#include "pal_vehicle_lowvolumemodule.h"

#define WAITING_FOR_SIGNALS_TIMEOUT 10  // seconds
#define TIMEOUT_BETWEEN_COMMANDS    2   // seconds


namespace {

class VehicleIntegrationTest : public ::testing::Test {

    protected:
    // You can remove any or all of the following functions if its body
    // is empty.

    VehicleIntegrationTest() {
        // You can do set-up work for each test here.

        //open_vehicle_bus();
    }

    virtual ~VehicleIntegrationTest() {
        // You can do clean-up work that doesn't throw exceptions here.

        //close_vehicle_bus();
    }

    // If the constructor and destructor are not enough for setting up
    // and cleaning up each test, you can define the following methods:

    virtual void SetUp() {
        // Code here will be called immediately after the constructor (right
        // before each test).
    }

    virtual void TearDown() {
        // Code here will be called immediately after each test (right
        // before the destructor).

        sleep(TIMEOUT_BETWEEN_COMMANDS);
     }

  // Objects declared here can be used by all tests in the test case for Foo.
};


//int set_camera_video_ics_display_active (pal_bool value) -- in pal_vehicle_camera.h
TEST_F(VehicleIntegrationTest, Camera) {
    sleep(WAITING_FOR_SIGNALS_TIMEOUT); // Waiting for open_vehicle_bus() to finish

    ASSERT_EQ(
        set_camera_video_ics_display_active(PAL_TRUE),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_camera_video_ics_display_active(PAL_FALSE),
        PAL_SUCCESS
    );
}

//int set_custom_mode_driveline_customization_change_setting_request(uint32_t value) -- in pal_vehicle_customization.h
TEST_F(VehicleIntegrationTest, Customization) {
    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_NO_ACTION),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_1),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_2),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_3),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_4),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_5),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_6),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_custom_mode_driveline_customization_change_setting_request(CSM_CUSTMDDRVLCSTCHNGSETREQ_CUSTOM_MODE_7_),
        PAL_SUCCESS
    );
}

//int set_hour_of_day(uint32_t value)  -- in pal_vehicle_dateandtime.h
TEST_F(VehicleIntegrationTest, DateAndTime) {
    //ASSERT_EQ(get_cellular_network_date_and_time_available(PAL_TRUE), PAL_SUCCESS);

    ASSERT_EQ(
        set_hour_of_day(0),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        set_hour_of_day(23),
        PAL_SUCCESS
    );
}

//int get_amplifier_sink_state_dsp_available(pal_bool *value)    -- in  pal_vehicle_audio.h
//int get_amplifier_sink_state_dsp_mode_0_present(pal_bool *value) -- in pal_vehicle_audio.h
TEST_F(VehicleIntegrationTest, Audio) {
    pal_bool value;

    ASSERT_EQ(
        get_amplifier_sink_state_dsp_available(&value),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        get_amplifier_sink_state_dsp_mode_0_present(&value),
        PAL_SUCCESS
    );
}

//int get_alternative_fuel_level_low(pal_bool *value) -- in  pal_vehicle_fuel.h
TEST_F(VehicleIntegrationTest, Fuel) {
    pal_bool value;

    ASSERT_EQ(
        get_alternative_fuel_level_low(&value),
        PAL_SUCCESS
    );
}

//int get_adaptive_cruise_control_auto_set_speed_status (uint32_t *value) -- in pal_vehicle_cruisecontrol.h
TEST_F(VehicleIntegrationTest, Cruisecontrol) {
    uint32_t value;

    ASSERT_EQ(
        get_adaptive_cruise_control_auto_set_speed_status(&value),
        PAL_SUCCESS
    );
}

//int get_low_volume_module_audio_video_request_application_state(uint32_t *value) -- in pal_vehicle_lowvolumemodule.h
TEST_F(VehicleIntegrationTest, AudioApplicationState) {
    uint32_t value;
    
    ASSERT_EQ(
        get_low_volume_module_audio_video_request_application_state(&value),
        PAL_SUCCESS
    );
    
    ASSERT_EQ(
        get_low_volume_module_audio_video_request_application_state(&value),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        get_low_volume_module_audio_video_request_application_state(&value),
        PAL_SUCCESS
    );

    ASSERT_EQ(
        get_low_volume_module_audio_video_request_application_state(&value),
        PAL_SUCCESS
    );
 
    ASSERT_EQ(
        get_low_volume_module_audio_video_request_application_state(&value),
        PAL_SUCCESS
    );
}

} // namespace