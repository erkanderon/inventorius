from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
import nmap, re

from django.core.mail import send_mail, BadHeaderError
from celery import current_task
import time
from subnet.models import NMAPTask, Subnet, Ip, Description


logger = get_task_logger(__name__)


@shared_task(bind=True)
def nmap_analyze(self, subnet_ip, mask):
    self.start = time.time()
    task = NMAPTask(task_id=self.request.id, flag="1")
    task.save()

    #nmap related
    cidr = "{}/{}".format(subnet_ip, mask)
    scanner = nmap.PortScanner()

    logger.info("NMAP analyze is starting for cidr " + str(subnet_ip) + "/" + str(mask))  
    try:
        scan_result = scanner.scan(hosts=cidr, arguments="-O")
        migrate(scan_result, cidr, subnet_ip, mask)
        logger.info("NMAP analyze is finished for cidr " + str(subnet_ip) + "/" + str(mask))
        end = time.time()
        NMAPTask.objects.filter(task_id=self.request.id).update(flag="0", took_time_in_minute=(end - self.start)/60)
    except Exception as e:
        logger.info("NMAP analyze is failed for cidr " + str(subnet_ip) + "/" + str(mask))
        logger.info(e)
        NMAPTask.objects.filter(task_id=self.request.id).update(flag="2", took_time_in_minute=(time.time() - self.start)/60)

    return

def migrate(data, cidr, subnet_ip, mask):
    for key, value in data["scan"].items():
        ip = value["addresses"]["ipv4"]
        subnet = Subnet.objects.filter(subnet_ip=subnet_ip, mask=mask, cidr=cidr).first()
        dns = value["hostnames"][0]["name"] if len(value["hostnames"][0]["name"]) > 0 else False
        description = None

        if dns:
        	description = search_for_regex(dns, description)

        port = serialize_port(value["tcp"])

        Ip.objects.update_or_create(ip=ip, subnet=subnet, dns=dns, description=description, port=port)

def search_for_regex(dns, description):
    descriptions = Description.objects.all()
    for i in descriptions.iterator():
        if re.search(i.regex, dns):
            description = i
            return description
    return description

def serialize_port(data):
    _port = ""
    for port, val in data.items():
        _port=_port + str(port) + ";"
    return _port