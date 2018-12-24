# Pull base image
FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

# COPY startup script into known file location in container
COPY start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# done!


# if on mac, run: "VBoxManage controlvm "development" natpf1 "tcp-port8000,tcp,,8000,,8000"; "
