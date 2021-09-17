#!/usr/bin/env python3
import argparse
import csv
import sys
from threading import Timer

import serial


class Options(object):

    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "serial_port", help="The RS232 port the simulator should send data to, e.g., /dev/com0")
        parser.add_argument(
            "filename", help="The path to a file, e.g., /path/to/file.txt")
        parser.add_argument(
            "period", default=0, type=float, help="The interval in which a line in the file should be read.")

        self.args = parser.parse_args(argv)

    def get_args(self):
        return vars(self.args)


class SimpleEmulator(object):
    def __init__(self):
        self.__serial_port = None
        self.__timer = None
        self.__file = None
        self.__current_line = 1

    @property
    def file(self) -> list:
        return self.__file

    @file.setter
    def file(self, filename: str) -> None:
        if filename is not None:
            with open(filename, 'r') as datafile:
                reader = csv.reader(datafile)
                headers = next(reader)
                self.__file = [{h: x for (h, x) in zip(headers, row)} for row in reader]

    def get_sample(self) -> None:
        new_value = self.read_next()
        self.serial_port.write(b''.join(new_value.values()))

    def read_next(self) -> dict:
        if self.__current_line + 1 > len(self.file):
            self.__current_line = -1
        self.__current_line += 1
        return self.file[self.__current_line + 1]

    @property
    def serial_port(self) -> serial.Serial:
        return self.__serial_port

    @serial_port.setter
    def serial_port(self, serial_port: str) -> None:
        try:
            self.__serial_port = serial.Serial(serial_port, baudrate=9200, timeout=0.5)  # open serial port
        except serial.SerialException:
            raise IOError("Problem connecting to serial device.")

    def server(self) -> None:
        try:
            while True:
                received_command = self.serial_port.readline().decode().rstrip().upper()
                if received_command is None:
                    continue
                elif received_command == 'GET_SAMPLE':
                    self.get_sample()
                elif received_command[0:5] == 'PERIOD':
                    period_command, value = received_command.split(' ')
                    if self.timer.isAlive():
                        self.timer.cancel()
                    self.timer = value
                    self.serial_port.write(b'SET NEW PERIOD: {} (seconds)'.format(value))
                else:
                    self.serial_port.write(b'Invalid Command')
        except serial.SerialException:
            print('Serial port is already opened or does not exist.')

    def start_emulator(self, serial_port, filename, period=None) -> None:
        self.serial_port = serial_port
        self.file = filename
        self.timer = period

        self.server()

    def stop_emulator(self) -> None:
        self.timer = 0
        self.serial_port.close()

    @property
    def timer(self) -> Timer:
        return self.__timer

    @timer.setter
    def timer(self, period: float) -> None:
        if self.__timer is not None:
            if self.__timer.isAlive():
                self.__timer.cancel()
        if period > 0:
            self.__timer = Timer(interval=period, function=self.get_sample)
            self.__timer.start()
        else:
            self.__timer = None


if __name__ == "__main__":
    emulator = None
    try:
        options = Options(sys.argv[1:])
        emulator = SimpleEmulator()
        emulator.start_emulator(options.args.serial_port, options.args.filename, options.args.period)
        print("Emulator was started")
    except KeyboardInterrupt:
        emulator.stop_emulator()
        print("Emulator was stopped")
        pass
