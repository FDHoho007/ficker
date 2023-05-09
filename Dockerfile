FROM debian

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y cron python3 python3-pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ficker.py .
COPY template_message.html .
COPY template_message.txt .
COPY template_subject.txt .

COPY crontab /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
