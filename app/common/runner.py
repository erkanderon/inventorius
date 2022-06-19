import re
from subnet.models import Ip
from .models import Description
from environment.models import Environment

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
        ip_count = Ip.objects.filter(description=env.regex).values("ip", "dns", "port").distinct().count()
        env.count = ip_count
        env.save()