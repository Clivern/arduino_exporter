.. image:: https://img.shields.io/pypi/v/arduino_exporter.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/arduino_exporter/
.. image:: https://github.com/Clivern/arduino_exporter/actions/workflows/ci.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/Clivern/arduino_exporter/actions/workflows/ci.yml

|

================
Arduino Exporter
================

    Arduino Prometheus Exporter



To use the exporter, follow the following steps

1. Create a python virtual environment.

.. code-block::

    $ python3 -m venv venv
    $ source venv/bin/activate


2. Install arduino_exporter package with pip.

.. code-block::

    $ pip install arduino_exporter


3. To run the exporter process.

.. code-block::

    $ python -m arduino_exporter.cli --p 8000
