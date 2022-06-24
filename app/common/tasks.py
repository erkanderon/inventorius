from celery.utils.log import get_task_logger
from celery import shared_task

from subnet.models import Ip
from .models import Description
from environment.models import Environment

from .runner import sync_environment_count as sync_env

logger = get_task_logger(__name__)

@shared_task(name='sync_ip_description', bind=True)
def sync_ip_description(*args):
    try:
        sync_env()
        logger.info("Sync IP Description Syncronization finished success")
    except Exception as e:
        logger.info("Sync IP Description Syncronization finished failed")
        logger.info(e)

@shared_task(name='sync_environment_count', bind=True)
def sync_environment_count(*args):
    try:
        sync_env()
        logger.info("Environment Count Syncronization finished success")
    except Exception as e:
        logger.info("Environment Count Syncronization finished failed")
        logger.info(e)

