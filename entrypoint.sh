#!/bin/sh
printenv | grep -v "no_proxy" >> /etc/environment
cron
python3 ficker.py >> /var/log/cron.log 2>&1
tail -f /var/log/cron.log
