REDIS_HOST = 'rainbowdash.lan'
REDIS_PORT = 6379
INTERFACES = ['lan']
PERIOD = 30
EXPIRATION = 300
INFLUX_HOST = ""

try:
    from local_config import *
except ImportError:
    pass
