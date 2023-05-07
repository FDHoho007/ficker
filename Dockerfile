FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ficker.py .
COPY template_message.html .
COPY template_message.txt .
COPY template_subject.txt .

COPY crontab /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

CMD ["crond", "&&", "tail", "-f", "/usr/src/app/log.txt"]