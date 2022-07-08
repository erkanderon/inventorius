import re
from subnet.models import Ip
from .models import Description
from environment.models import Environment

import socket
import errno

def sync_ip_description():
    descriptions = Description.objects.all()
    ip = Ip.objects.all()
    for ip_obj in ip.iterator():
        for desc in descriptions.iterator():
            if re.search(desc.regex, ip_obj.dns):
                ip_obj.description.add(desc)
        ip_obj.save()

def sync_environment_count():
    environments = Environment.objects.all()
    for env in environments.iterator():
        ip_count = Ip.objects.filter(description=env.regex)
        env.count = len(ip_count)
        env.save()

def check_machine_connection(dns, port):
    status = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(2)
    try:
        code = sock.connect_ex((dns, port))
    except socket.gaierror:
        return 1001, 0
    if code == 0:
        status = 1
    sock.close()
    return code, status