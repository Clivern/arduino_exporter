.. image:: https://img.shields.io/pypi/v/arduino_exporter.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/arduino_exporter/
.. image:: https://github.com/Clivern/arduino_exporter/actions/workflows/ci.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/Clivern/arduino_exporter/actions/workflows/ci.yml

|

===========================
Arduino Prometheus Exporter
===========================

You can run this exporter on a device (PC or Raspberry PI) connected to an arduino. The exporter will listen to messages sent over the serial port and update the metrics exposed to prometheus.
I used this project to visualize and trigger alerts for a lot of sensors values like sound, temperature and water level ... etc

To use the exporter, follow the following steps:

1. Create a python virtual environment.

.. code-block::

    $ python3 -m venv venv
    $ source venv/bin/activate


2. Install arduino-exporter package with pip.

.. code-block::

    $ pip install arduino-exporter


3. To run the arduino exporter process. You can use systemd to run the process on PC or Raspberry PI. The serial port value can be retrieved from arduino IDE.

.. code-block::

    $ arduino_exporter server run -s $serial_port -p $http_port
    $ arduino_exporter server run -s /dev/cu.usbmodem14101 -p 8000


4. Upload a sketch to the arduino to send the metrics to the serial port.

.. code-block::

    #define LED 13

    void setup() {
      Serial.begin(9600);
      pinMode(LED, OUTPUT);
    }

    void loop() {
      digitalWrite(LED, HIGH);
      delay(1000);
      digitalWrite(LED, LOW);
      delay(1000);
      Serial.write("{\"type\": \"gauge\", \"name\": \"room_temp\", \"help\": \"the room temperature.\", \"method\": \"set\", \"value\": 14.3, \"labels\": {\"place\": \"us\"}}");
    }
