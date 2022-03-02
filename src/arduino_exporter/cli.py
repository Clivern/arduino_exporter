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

import argparse
import logging
import sys
import time

from arduino_exporter import __version__
from arduino_exporter.serial import Serial
from arduino_exporter.server import Server
from arduino_exporter.prometheus import Prometheus


__author__ = "Clivern"
__copyright__ = "Clivern"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

def parse_args(args):
    """
    Parse command line parameters

    Args:
        args (List[str]): command line parameters as list of strings
            (for example  ``["--help"]``).

    Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Arduino Prometheus Exporter")

    parser.add_argument(
        "--version",
        action="version",
        version="arduino_exporter {ver}".format(ver=__version__),
    )

    parser.add_argument(
        dest="operation",
        help="The command to execute",
        type=str, metavar="STR"
    )

    parser.add_argument(
        dest="serial_port",
        help="The serial port to listen to",
        type=str,
        metavar="STR"
    )

    parser.add_argument(
        "--p",
        dest="port",
        help="The HTTP server port",
        type=int,
        metavar="INT",
        default=8000
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="Set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="Set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """
    Setup basic logging

    Args:
        loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"

    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)

    setup_logging(args.loglevel)

    _logger.info("Arduino exporter cli command {}".format(args.operation))

    if args.operation == "run":
        _logger.info("Starting arduino exporter HTTP server on port {}".format(args.port))
        server = Server(args.port)
        prometheus = Prometheus()

        server.add_callback(lambda: time.sleep(1))
        server.add_callback(lambda: prometheus.store('{"type": "counter", "name": "app_orders", "help": "the amount of orders.", "method": "inc", "value": 1, "labels": {"type": "trousers"}}'))

        server.run()

    else:
        raise Exception("Invalid opertaion name {}".format(args.operation))

    _logger.info("Arduino exporter HTTP server stopped")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
