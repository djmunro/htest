import threading
import tempfile
import shutil
import serial
import time
import sys
import os


class TimeoutException(Exception):
    pass


class SerialConsoleCommand:
    def __init__(self, command=None, prompt='$', serial=None):
        if not serial:
            raise ValueError("A Serial instance must be passed to SerialConsoleCommand.")

        self.serial =  serial
        self.set_prompt(prompt)
        self.buffer = []
        if command:
            self.execute(command)

    def set_prompt(self, prompt):
        self.prompt = prompt

    def execute(self, command):
        self.finished = False
        self.buffer = []
        self.serial.write(command + '\r')
        while not self.finished:
            pass
        return '\n'.join(self.buffer)

    def callback(self, line):
        if not self.prompt in line:
            self.buffer.append(line)
        else:
            self.finished = True

class SerialConsoleLineFinder:
    def __init__(self, text=None):
        self.setFindText(text)
        self.found = False
        self.text = None

    def setFindText(self, text=None):
        self.text = text
        self.found = False
        self.buffer = []

    def callback(self, line):
        if not self.found and self.text != None:
            if not type(self.text) == type([]):
                self.text = [self.text]
            matched = False
            try:
                for signal in self.text:

                    if signal in line:
                        self.text.remove(signal)

                # We've matched everything if the list is empty
                matched = self.text == []
            except UnicodeDecodeError as e:
                print "Error matching text %s to line %s" % (self.text, repr(line))
                print "Unicode error is %s" % e

            if matched:
                self.found = True
                self.text = None
            self.buffer.append(line)

    def wait_for_text(self, text=None, timeout=30.0, return_buffer=False, _assert=True):
        if not text:
            if not self.text and not self.found:
                raise ValueError("No text to search specified.")

        if text:
            self.setFindText(text or self.text)

        start = time.clock()
        while (time.clock() - start) < timeout:
            if self.found:
                self.text = None
                if return_buffer:
                    return "\n".join(self.buffer)
                else:
                    return self.buffer[-1]

        if _assert:
            raise ValueError("Text (%s) was not found within the specified timeout (%s)" % (self.text, timeout))
        else:
            return "\n".join(self.buffer)

class SerialConsoleLogger:
    def __init__(self, timestamp=True):
        self.timestamp = timestamp
        self.outfile = None

    def callback(self, line):
        if self.outfile:
            if self.timestamp:
                stamp = "[%s] " % time.asctime()
            else:
                stamp = ''
            self.outfile.write("%s%s\r\n" % (stamp, line.strip()))

    def startLogging(self):
        self.clearLogging()

    def stopLogging(self):
        self.outfile = None

    def clearLogging(self):
        self.outfile = tempfile.NamedTemporaryFile(delete=False)

    def getLogFile(self):
        tmp = ""
        if self.outfile:
            # Null the outfile so we don't try to write to it
            tmp = self.outfile
            self.outfile = None
            tmp.close()
        else:
            print "Warning, no serial logs were available! (Buffer was empty.)"
        return tmp.name

    def saveLogs(self, out_location):
        if self.outfile:
            rootDir = os.path.split(out_location)[0]
            if not os.path.isdir(rootDir):
                raise ValueError("Invalid file location %s" % rootDir)

            # Null the outfile so we don't try to write to it
            tmp = self.outfile
            self.outfile = None
            tmp.close()

            # Copy the file
            shutil.copy(tmp.name, out_location)
        else:
            print "Warning, no serial logs were available! (Buffer was empty.)"

class SerialConsole2:
    #prevents RF from creating a new instance for every test case
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, comport, baud=115200):
        # Initialize data members
        self.baud = int(baud)
        self.port = int(comport)
        self.thread = None
        self.callbacks = []
        self.exit = False

        # Fix for linux COM paths
        if 'linux' in sys.platform:
                self.port = '/dev/ttyUSB' + str(self.port)
        else:
            # We should still accept 1-indexed comports in Windows
            self.port -= 1

        self.connect_serial()

        # Initialize handlers
        self.sclf = SerialConsoleLineFinder()
        self._register_callback(self.sclf.callback)

        self.scl = SerialConsoleLogger()
        self._register_callback(self.scl.callback)

        self.ce = SerialConsoleCommand(serial=self.serial)
        self._register_callback(self.ce.callback)

    # Connect, Disconnect Methods
    def connect_serial(self):

        self.serial = serial.Serial(port = self.port,
                                    baudrate = self.baud,
                                    timeout = 0.5)

        self.exit = False
        self.thread = threading.Thread(target=self._runThread)
        self.thread.setDaemon(True)
        self.thread.start()

    def disconnect_serial(self):
        self.serial.close()
        self.serial = None
        self.exit = True

    # Callbacks and housekeeping
    def _call_callbacks(self, line):
        for callback in self.callbacks:
            callback(line)

    def _runThread(self):
        while not self.exit:
            line = None
            try:
                line = self.serial.readline()
            except serial.SerialTimeoutException as e:
                pass
            except serial.SerialException as e:
                pass

            if line:
                self._call_callbacks(line.strip())

    def _register_callback(self, callback):
        self.callbacks.append(callback)

    # Logging methods
    def start_serial_logging(self):
        self.scl.startLogging()

    def stop_serial_logging(self):
        self.scl.stopLogging()

    def clear_serial_logs(self):
        self.scl.clearLogging()

    def save_serial_logs(self, out_location):
        self.scl.saveLogs(out_location)

    def get_serial_logs(self):
        return self.scl.getLogFile()

    # Serial wait methods
    def wait_for_serial_text(self, text=None, timeout=30.0, _assert=True):
        return self.sclf.wait_for_text(text, timeout, _assert=_assert)

    def wait_for_serial_text_and_get_buffer(self, text=None, timeout=30.0, _assert=True):
        return self.sclf.wait_for_text(text, timeout, _assert=_assert, return_buffer=True)

    def set_serial_wait_text(self, text):
        self.sclf.setFindText(text)

    # Command Methods
    def set_serial_prompt(self, prompt):
        self.ce.set_prompt(prompt)

    def execute_serial_command(self, command):
        return self.ce.execute(command)

    def write_to_serial(self, command):
        self.serial.write(command)

    def serial_login(self, login='root', password=None, login_prompt='login:', pass_prompt='Password:'):
        # hit enter and read nextline. if prompt.. we're logged in?

        try:
            self.set_serial_wait_text(login_prompt)
            self.write_to_serial('\n')
            self.wait_for_serial_text(timeout=5)
            self.set_serial_wait_text(pass_prompt)
            self.write_to_serial(login + '\n')

            if password:
                self.write_to_serial(password + '\n')
                self.wait_for_serial_text(self.ce.prompt)

        except ValueError:
            print("Already logged in")

        except:
            raise TimeoutException("Wasn't able to successfully connect to serial")

        print("Login successful!")