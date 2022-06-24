#!/bin/bash
kill -9 $(ps -ef | grep -i manage.py | grep -v grep | awk '{print $2}')