from celery.utils.log import get_task_logger
from celery import shared_task

from subnet.models import Ip
from .models import Description
from environment.models import Environment

from .runner import sync_environment_count, sync_ip_description, check_watcher_status, send_machine_status_alarm

from .models import Description, NetworkConnDescription
from environment.models import Environment
from watcher.models import Watcher

import socket
import errno

logger = get_task_logger(__name__)

@shared_task(name='sync_ip_description', bind=True)
def sync_ip_description_task(*args):
    try:
        sync_ip_description()
        logger.info("Sync IP Description Syncronization finished success")
    except Exception as e:
        logger.info("Sync IP Description Syncronization finished failed")
        logger.info(e)

@shared_task(name='sync_environment_count', bind=True)
def sync_environment_count_task(*args):
    try:
        sync_environment_count()
        logger.info("Environment Count Syncronization finished success")
    except Exception as e:
        logger.info("Environment Count Syncronization finished failed")
        logger.info(e)

@shared_task(name='check_watcher_status', bind=True)
def check_watcher_status_task(*args):
    try:
        check_watcher_status()
        logger.info("Watcher Status analyze finished success")
    except Exception as e:
        logger.info("Watcher Status analyz finished failed")
        logger.info(e)

@shared_task(name='machine_status_alarm', bind=True)
def machine_status_alarm_task(*args):
    try:
        send_machine_status_alarm()
        logger.info("Machine Status Alarm Task finished success")
    except Exception as e:
        logger.info("Machine Status Alarm Task finished failed")
        logger.info(e)


