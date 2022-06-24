#!/bin/bash
kill -9 $(ps -ef | grep -i celery | grep -i worker | grep -v grep | awk '{print $2}')