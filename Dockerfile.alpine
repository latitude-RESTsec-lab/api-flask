FROM python:3-alpine3.6

ENV http_proxy 'http://10.30.0.10:3128'
ENV https_proxy 'https://10.30.0.10:3128'

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --proxy='https://10.30.0.10:3128' --no-cache-dir -r requirements.txt

ADD src /app

ADD ./devssl ./devssl

COPY database.conf database.conf

EXPOSE 8000

ENTRYPOINT ["/bin/ash", "run.sh"]
