REDIS_HOST = 'rainbowdash.lan'
REDIS_PORT = 6379
INTERFACES = ['eth0']
PERIOD = 30
EXPIRATION = 300
MOCK = False

try:
    from local_config import * # NOQA
except ImportError:
    pass
