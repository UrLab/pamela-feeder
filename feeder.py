from redis import StrictRedis
from config import (REDIS_HOST, REDIS_PORT, INTERFACES, PERIOD, EXPIRATION,
                    INFLUX_HOST, MOCK)
import subprocess
import re
from periodic import periodic
from datetime import datetime
import requests

ARP_REGEX = r"(?P<host>^\S+) \((?P<ip>(\d{1,3}\.){3}\d{1,3})\) at (?P<mac>((\d|[a-f]){2}:){5}(\d|[a-f]){2}) \[\w+\] on (?P<interface>\S+)$"
ARP_REGEX = re.compile(ARP_REGEX)

ANDROID_REGEX = r"^(?P<android>android)-(?P<id>[0-9a-fA-F]+)$"
ANDROID_REGEX = re.compile(ANDROID_REGEX)


def get_redis():
    return StrictRedis(REDIS_HOST, REDIS_PORT)


def send_mac(client, maclist):
    payload = ','.join(maclist)
    client.setex('incubator_pamela', EXPIRATION, payload)
    if INFLUX_HOST:
        try:
            requests.post(
                INFLUX_HOST,
                data='mac_count value={}'.format(len(maclist)),
                headers={'Accept-encoding': 'identity'}
            )
        except:
            print(datetime.now(), "Error when sending people count to influx")


def send_hostnames(client, hosts_dict):
    if hosts_dict:
        client.hmset("incubator_pamela_hostnames", hosts_dict)


def get_mac(*interfaces):
    if MOCK:
        with open("arp.mock", "r") as m:
            stdout = m.read()
    else:
        stdout = subprocess.check_output(['sudo', 'arp', '-a'])
    stdout = stdout.split('\n')
    valid = filter(lambda x: "<incomplete>" not in x, stdout)
    valid = filter(lambda x: x.strip() != "", valid)

    out = []

    for line in valid:
        match = re.match(ARP_REGEX, line)
        if match:
            machine = match.groupdict()
            if machine['interface'] in interfaces:
                out.append(machine)

    return out


def strip_suffix(s, suf):
    if s.endswith(suf):
        return s[:-len(suf)]
    return s


def strip_prefix(s, pre):
    if s.startswith(pre):
        return s[len(pre):]
    return s


def is_host(host):
    if "?" in host:
        return False
    if len(host) < 3:
        return False

    return True


def format_host(host):
    host = strip_suffix(host, ".lan.urlab.be")
    host = strip_suffix(host, ".lan")
    host = strip_suffix(host, ".local")

    host = strip_suffix(host, "iPodtouch")
    host = strip_suffix(host, "-PC")
    host = strip_suffix(host, "-pc")

    host = strip_prefix(host, "pc-")
    host = strip_prefix(host, "PC-")
    
    host = strip_prefix(host, "LAPTOP-")
    host = strip_prefix(host, "iPod-de-")

    # if host.startswith("android"):
    #     match = re.match(ANDROID_REGEX, host)
    #     if match:
    #         host = "unknown-android"
    #     else:
    #         host = strip_prefix(host, "android-")
    return host


@periodic(PERIOD)
def main(client):
    macdicts = get_mac(*INTERFACES)

    maclist = [x['mac'] for x in macdicts]
    send_mac(client, maclist)

    hostnames = {x['mac']: format_host(x['host']) for x in macdicts if is_host(x['host'])}
    send_hostnames(client, hostnames)

if __name__ == '__main__':
    client = get_redis()
    client.set("incubator_pamela_expiration", EXPIRATION)
    main(client)
