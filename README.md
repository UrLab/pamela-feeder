# Pamela feeder

Pamela feeder is a simple Python (2 or 3) script that collects MAC adresses on the local network (currently via arp) and pushes them to a Redis server.

This will then be used by the incubator and the spaceapi to show who is in the space :)

## How to

    virtualenv ve
    pip install -r requirements.txt
    python feeder.py

To configure pamela-feeder, you may override configuration options from `config.py` in a `local_config.py` file in the same directory.

## Technical details

A string containing MAC addresses separated by a comma is stored in a key named `incubator_pamela` with a TTL of 5m
