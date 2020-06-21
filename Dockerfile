#FROM python:2
#ADD aidon_elastic.py /
#ADD aidon_obis.py /
#RUN pip install elasticsearch crcmod pyserial
#CMD [ "python", "./aidon_elastic.py", "/dev/ttyUSB0" ]

# Container image that runs your code
FROM alpine:3.10

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]