FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ficker.py .
COPY template_message.html .
COPY template_message.txt .
COPY template_subject.txt .

CMD [ "python", "./ficker.py" ]