#!/bin/bash
export PYTHONPATH="/Application/Inventorius/inventorius/app/:$PYTHONPATH"
nohup celery -A app beat --loglevel=info > /Application/Inventorius/celery.out &