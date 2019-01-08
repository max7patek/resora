# Pull base image
FROM ubuntu:latest

# Install Python 3.6
RUN apt-get update
RUN apt-get install -y cron
RUN apt-get install -y python3.6 python3.6-dev python3-pip && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED 1

# Import code and pip install
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
ADD ./secrets/service_creds.json /secrets/service_creds.json
ADD ./secrets/databaseconfig /secrets/databaseconfig

# Add crontab file in the cron directory
ADD cronfile /etc/cron.d/cronfile

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronfile

# Apply cron job
RUN crontab /etc/cron.d/cronfile

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# COPY startup script into known file location in container
COPY start.sh /start.sh

# done!


# if on mac, run: "VBoxManage controlvm "<machine name>" natpf1 "tcp-port8000,tcp,,8000,,8000"; "
