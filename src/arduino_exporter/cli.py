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

import click
import time

from arduino_exporter import __version__
from arduino_exporter.serial import Serial
from arduino_exporter.server import Server
from arduino_exporter.prometheus import Prometheus


@click.group(help="🐺 Arduino Prometheus Exporter")
@click.version_option(version=__version__, help="Show the current version")
def main():
    pass


# Server command
@click.group(help="Server commands")
def server():
    pass


# Run server sub command
@server.command(help="Run server")
@click.option(
    "-s",
    "--serial",
    "serial",
    type=click.STRING,
    default="",
    required=True,
    help="The Serial port to listen to",
)
@click.option(
    "-p",
    "--port",
    "port",
    type=click.INT,
    default=8000,
    help="The HTTP server port",
)
@click.option(
    "-b",
    "--baud",
    "baud",
    type=click.INT,
    default=9600,
    help="The Serial communication baud rate",
)
def run(serial, baud, port):
    try:
        print(f"Starting server on port {port}")
        server = Server(int(port))
        prometheus = Prometheus()
        serial = Serial(serial, baud)

        server.add_callback(lambda: time.sleep(1))
        server.add_callback(lambda: prometheus.store(serial.read()))
        server.run()
    except Exception as e:
        raise click.ClickException("Error while running the server: {}".format(str(e)))


# Register Commands
main.add_command(server)


if __name__ == "__main__":
    main()
