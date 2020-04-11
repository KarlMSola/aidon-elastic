FROM python:2

ADD aidon_elastic.py /
ADD aidon_obis.py /

RUN pip install elasticsearch crcmod pyserial

CMD [ "python", "./aidon_elastic.py", "/dev/ttyUSB0" ]
