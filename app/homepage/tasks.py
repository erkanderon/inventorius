from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail, BadHeaderError
from celery import current_task
import time
from homepage.models import NMAPTask


logger = get_task_logger(__name__)

@shared_task(bind=True)
def nmap_analyze(self, subnet_ip, mask):
    self.start = time.time()
    task = NMAPTask(task_id=self.request.id, flag="1")
    task.save()
    logger.info("NMAP analyze is starting for cidr " + str(subnet_ip) + "/" + str(mask))
    time.sleep(10)
    logger.info("NMAP analyze is finished for cidr " + str(subnet_ip) + "/" + str(mask))
    end = time.time()
    NMAPTask.objects.filter(task_id=self.request.id).update(flag="0", took_time_in_minute=(end - self.start)/60)
    return
