from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail, BadHeaderError
from celery import current_task
import time


logger = get_task_logger(__name__)


@shared_task(bind=True)
def add_function(self, x, y):
    print("Started task")
    time.sleep(10)
    print(x+y)
    logger.info("Sumed")
    print("Task is ended")
    return x+y

@shared_task(bind=True)
def nmap_analyze(self, subnet_ip, mask):
    logger.info("NMAP analyze is starting for cidr " + str(subnet_ip) + "/" + str(mask))
    time.sleep(200)
    logger.info("NMAP analyze is finished for cidr " + str(subnet_ip) + "/" + str(mask))
    return