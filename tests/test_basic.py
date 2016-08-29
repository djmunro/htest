from __future__ import unicode_literals, absolute_import

import logging
import os
import subprocess
import unittest

import adb

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


IMAGE_FIXTURES = os.path.join(os.path.dirname(__file__), 'image_fixture/')



def power_on():
    import can

    can.rc['interface'] = 'socketcan_ctypes'

    msg = can.Message(extended_id=False, arbitration_id=0x621, data=[0, 0x40, 0, 0, 0, 0, 0, 0])
    # msg = can.Message(data=b'621#0040000000000000')

    task = can.send_periodic('can0', msg, 3)
    task.start()


class GmPowermodingTests(unittest.TestCase):

    def setUp(self):
        power_on()

        adb.connect('192.168.0.123')
        adb.push("../bin/pal-integration-playground", "/data/")

    def tearDown(self):
        #adb.disconnect('192.168.0.123')
        pass

    def testLowFuel(self):
        print("Running Low fuel test")
        output = subprocess.Popen([
            "adb", "shell", "./data/pal-integration-playground", "--gtest_filter=*Fuel*"
        ], stdout=subprocess.PIPE).communicate()[0]

        logger.info(output)


if __name__ == '__main__':
    unittest.main()
