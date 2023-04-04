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

import json

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram
from prometheus_client import Info
from prometheus_client import Enum


class Prometheus:
    """Prometheus Class"""

    def __init__(self):
        self.metrics = {}

    def store(self, data):
        """
        Expose a data object

        Args:
            data: The data has the following format
                {
                    "type": "counter",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "method": "inc",
                    "value": 1,
                    "labels": {
                        "type": "trousers"
                    }
                }
        """

        if data is None:
            return

        # Avoid any bad input
        try:
            item = json.loads(data.strip())
        except Exception:
            print(f"Invalid data received {data}")
            return

        value = "---"
        typ = item["type"]

        if "value" in item.keys():
            value = item["value"]

        print(f"New metric received with type {typ} with value {value}")

        if "help" not in item.keys():
            item["help"] = ""

        if "labels" not in item.keys():
            item["labels"] = {}

        if item["type"] == "counter" or item["type"] == "c":
            self.counter(item)
        elif item["type"] == "gauge" or item["type"] == "g":
            self.gauge(item)
        elif item["type"] == "summary" or item["type"] == "s":
            self.summary(item)
        elif item["type"] == "histogram" or item["type"] == "h":
            self.histogram(item)
        elif item["type"] == "info" or item["type"] == "i":
            self.info(item)
        elif item["type"] == "enum" or item["type"] == "e":
            self.enum(item)

    def counter(self, item):
        """
        Prometheus Counter

        Args:
            item: The metric data
                {
                    "type": "counter",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "method": "inc",
                    "value": 1,
                    "labels": {
                        "type": "trousers"
                    }
                }
        """
        c = None

        for name, metric in self.metrics.items():
            if name == item["name"]:
                c = metric

        if c is None:
            c = Counter(item["name"], item["help"], item["labels"].keys())
            c = c.labels(*item["labels"].values())

        c.inc(item["value"])
        self.metrics[item["name"]] = c
        return c

    def gauge(self, item):
        """
        Prometheus Gauge

        Args:
            item: The metric data
                {
                    "type": "gauge",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "method": "inc", # inc or dec or set
                    "value": 1,
                    "labels": {
                        "type": "trousers"
                    }
                }
        """
        g = None

        for name, metric in self.metrics.items():
            if name == item["name"]:
                g = metric

        if g is None:
            g = Gauge(item["name"], item["help"], item["labels"].keys())
            g = g.labels(*item["labels"].values())

        if item["method"] == "inc":
            g.inc(item["value"])
        elif item["method"] == "dec":
            g.dec(item["value"])
        elif item["method"] == "set":
            g.set(item["value"])

        self.metrics[item["name"]] = g

        return g

    def summary(self, item):
        """
        Prometheus Summary

        Args:
            item: The metric data
                {
                    "type": "summary",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "method": "observe",
                    "value": 1,
                    "labels": {
                        "type": "trousers"
                    }
                }
        """
        s = None

        for name, metric in self.metrics.items():
            if name == item["name"]:
                s = metric

        if s is None:
            s = Summary(item["name"], item["help"], item["labels"].keys())
            s = s.labels(*item["labels"].values())

        s.observe(item["value"])
        self.metrics[item["name"]] = s
        return s

    def histogram(self, item):
        """
        Prometheus Histogram

        Args:
            item: The metric data
                {
                    "type": "histogram",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "method": "observe",
                    "value": 1,
                    "labels": {
                        "type": "trousers"
                    }
                }
        """
        h = None

        for name, metric in self.metrics.items():
            if name == item["name"]:
                h = metric

        if h is None:
            h = Histogram(item["name"], item["help"], item["labels"].keys())
            h = h.labels(*item["labels"].values())

        h.observe(item["value"])
        self.metrics[item["name"]] = h
        return h

    def info(self, item):
        """
        Prometheus Info

        Args:
            item: The metric data
                {
                    "type": "info",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "value": {'version': '1.2.3', 'buildhost': 'foo@bar'}
                }
        """
        i = None

        for name, metric in self.metrics.items():
            if name == item["name"]:
                i = metric

        if i is None:
            i = Info(item["name"], item["help"])

        i.info(item["value"])
        self.metrics[item["name"]] = i
        return i

    def enum(self, item):
        """
        Prometheus Enum

        Args:
            item: The metric data
                {
                    "type": "enum",
                    "name": "app_orders",
                    "help": "the amount of orders.",
                    "states": ['starting', 'running', 'stopped'],
                    "state": 'starting'
                }
        """
        e = None

        for name, metric in self.metrics.items():
            if name == item["name"]:
                e = metric

        if e is None:
            e = Enum(item["name"], item["help"], states=item["states"])

        e.state(item["state"])
        self.metrics[item["name"]] = e
        return e
