import socket, os, re


def get_ip_addresses():
    """Returns a list of all the ip adresses of the local network"""
    addresses = []
    for device in os.popen("arp -a"):
        device = re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", device, re.M | re.I)
        if device is not None:
            addresses.append(device.group(0))
    return addresses


def get_servers(timeout=0.1):
    """Returns a list of all servers you can connect to."""
    available = []

    for ip in get_ip_addresses():
        print(ip)
        for port in range(0, 10000, 100):
            s = socket.socket()
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
            except ConnectionRefusedError:
                break
            except OSError:
                continue
            except socket.timeout:
                continue

            available.append((ip, port))

    return available


print(get_servers())
