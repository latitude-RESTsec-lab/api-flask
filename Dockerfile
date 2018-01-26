FROM python:3

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --proxy='https://10.30.0.10:3128' --no-cache-dir -r requirements.txt

ADD src /app

COPY database.conf database.conf

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "run.sh"]
