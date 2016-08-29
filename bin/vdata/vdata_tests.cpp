#include <gtest/gtest.h>
#include <unistd.h>
#include <stdlib.h>

#include "pal_vehicle_fuel.h"

#define TIMEOUT 30	// seconds

TEST(VehicleIntegrationTest, Fuel) {
    // uint32_t val;

    // ASSERT_EQ(
    //     get_adaptive_cruise_control_auto_set_speed_status(&val),
    //     PAL_SUCCESS
    // );

    pal_bool value;

    ASSERT_EQ(
    	get_alternative_fuel_level_low(&value),
    	PAL_SUCCESS
  	);

        printf("Sending CAN MESSAGE 000#FF000088AA00\n");
        system("./data/hdb 000#FF000088AA00");
        printf("Sent!\n");

}
