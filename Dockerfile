FROM python:3

# Install Ubuntu packages
#RUN apt-get update
#RUN apt-get install alien dpkg-dev debhelper build-essential libaio1 --assume-yes

# Install packages
#RUN dpkg -i *.deb

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --proxy='https://10.30.0.10:3128' --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
ENTRYPOINT [ "python3" ]
CMD [ "src/main.py" ]
