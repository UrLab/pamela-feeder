REDIS_HOST = 'rainbowdash.lan'
REDIS_PORT = 6379
INTERFACES = ['eth0']

try:
    from local_config import *
except ImportError:
    pass
