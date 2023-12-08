# MIT License
#
# Copyright (c) 2022 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import serial


class Serial:
    """Serial Class"""

    def __init__(self, serial_port, baud_rate):
        self._serial_port = serial_port
        self._serial = serial.Serial(self._serial_port, baud_rate, timeout=1)

    def read(self):
        """
        Read a line from a serial port

        Returns:
            The string value
        """

        line = self._serial.readline()

        if line:
            return line.decode()

    def write(self, message):
        """
        Write into serial port

        Args:
            message: The message to send
        """
        self._serial.write(bytes(message, "utf-8"))

    def close(self):
        """
        Close the serial port
        """
        self._serial.close()
