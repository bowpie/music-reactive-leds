import struct
import time
import serial
import logging


class ArduinoSerial:
    logger = logging.getLogger(__name__)

    def __init__(self, port, baudrate=115200, timeout=0.05, debug=False):
        # debug = False - running , else not running
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._debug = debug
        if self._debug:
            ArduinoSerial.logger.info("Debug mode is ON, arduino not running.")

    def debug(func):
        def inner_func(self, *args):
            if self._debug == False:
                if args:
                    func(self, *args)
                else:
                    func(self)

        return inner_func

    @debug
    def start_serial(self):

        ArduinoSerial.logger.info("Serial communication has started.")

        self.serial_com = serial.Serial(
            port=self._port, baudrate=self._baudrate, timeout=self._timeout
        )
        time.sleep(0.5)

    @debug
    def stop_serial(self):
        ArduinoSerial.logger.info("Serial communication has stopped.")

        self.serial_com.close()

    @debug
    def communicate(self, rgb: tuple):
        r, g, b = rgb
        self.serial_com.write(struct.pack(">B", r))
        self.serial_com.write(struct.pack(">B", g))
        self.serial_com.write(struct.pack(">B", b))
