from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
import nmap, re

from django.core.mail import send_mail, BadHeaderError
from celery import current_task
import time
from subnet.models import NMAPTask, Subnet, Ip, Description
from common.runner import sync_environment_count


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
        scan_result = scanner.scan(hosts=cidr, arguments="-O -p-")
        migrate(scan_result, cidr, subnet_ip, mask)
        logger.info("NMAP analyze is finished for cidr " + str(subnet_ip) + "/" + str(mask))
        end = time.time()
        NMAPTask.objects.filter(task_id=self.request.id).update(flag="0", took_time_in_minute=(end - self.start)/60)
    except Exception as e:
        logger.info("NMAP analyze is failed for cidr " + str(subnet_ip) + "/" + str(mask))
        logger.info(e)
        raise e
        NMAPTask.objects.filter(task_id=self.request.id).update(flag="2", took_time_in_minute=(time.time() - self.start)/60)

    return

def migrate(data, cidr, subnet_ip, mask):
    for key, value in data["scan"].items():
        try:
            ip = value["addresses"]["ipv4"]
            subnet = Subnet.objects.filter(subnet_ip=subnet_ip, mask=mask, cidr=cidr).first()
            dns = value["hostnames"][0]["name"] if len(value["hostnames"][0]["name"]) > 0 else ""
            description = None

            print("ip: {} - subnet: {} - dns: {} - desc: {}".format(ip, subnet, dns, description))

            port = serialize_port(value)

            update_or_create_ip(ip, subnet, dns, description, port)
            sync_environment_count()
        except Exception as e:
            raise e
            print("Bu value için hata alındı!!! {} - Hata: {}".format(value, e))
            continue

def serialize_port(data):
    _port = ""

    if not "tcp" in data:
        return _port

    for port, val in data["tcp"].items():
        _port=_port + str(port) + ";"
    return _port

def update_or_create_ip(ip, subnet, dns, description, port):
    try:
        obj = Ip.objects.get(
            ip=ip, # test with other fields if you want
            subnet=subnet
        )
        obj.dns = dns
        obj.port = port
        obj = search_for_regex(obj, dns, description)
        obj.save()
    except Ip.DoesNotExist:
        obj = Ip.objects.create(ip=ip, subnet=subnet, dns=dns, port=port)
        obj = search_for_regex(obj, dns, description)
        obj.save()

def search_for_regex(obj, dns, description):
    descriptions = Description.objects.all()
    for i in descriptions.iterator():
        if re.search(i.regex, dns):
            obj.description.add(i)
    return obj