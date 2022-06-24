#!/bin/bash
export PYTHONPATH="/Application/Inventorius/inventorius/app/:$PYTHONPATH"
nohup celery -A app worker --loglevel=INFO > /Application/Inventorius/celery.out &