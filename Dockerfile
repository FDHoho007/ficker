FROM debian:11-slim

RUN apt-get update && apt-get install -y cron python3 python3-pip

WORKDIR /root
COPY entrypoint.sh .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ficker.py .
COPY template_message.html .
COPY template_message.txt .
COPY template_subject.txt .

COPY ficker.cron /etc/cron.d/ficker.cron
RUN crontab /etc/cron.d/ficker.cron
RUN touch /var/log/cron.log

ENTRYPOINT ["/root/entrypoint.sh"]
