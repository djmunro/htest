import os
import logging

logger = logging.getLogger(__name__)


def connect(device):
    return _exec_command("connect {}".format(device))


def disconnect(device):
    return _exec_command("disconnect {}".format(device))


def root():
    return _exec_command("root")


def shell(cmd):
    return _exec_command("shell {}".format(cmd))


def push(local, remote):
    return _exec_command("push {} {}".format(local, remote))


def devices():
    result = _exec_command("devices")
    devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
    return [device for device in devices if len(device) > 2]


def _exec_command(cmd):
    result = ''

    logger.info("Executing '{command}' command".format(command=cmd))

    res = os.popen('adb {}'.format(cmd), "r")
    while 1:
        line = res.readline()
        if not line:
            break
        result += line

    return result

