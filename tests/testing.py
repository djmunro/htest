from __future__ import unicode_literals, absolute_import

import os
import unittest
import adb
import logging
import subprocess
import time

from cereal import SerialConsole2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


IMAGE_FIXTURES = os.path.join(os.path.dirname(__file__), 'image_fixture/')


class Foo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLowFuel(self):
        print("Running Low fuel test")
        proc = subprocess.Popen([
            "adb", "shell", "logcat"
        ], stdout=subprocess.PIPE)

        while True:
            line = proc.stdout.readline()
            if line != '':
                # the real code does filtering here
                print "test:", line.rstrip()
            else:
                break


if __name__ == '__main__':
    unittest.main()
