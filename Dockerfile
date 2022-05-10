FROM tensorflow/tensorflow:latest-gpu
#FROM tensorflow/tensorflow:2.4.0rc3-gpu


RUN mkdir /temp
COPY requirements.txt /temp/requirements.txt
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN python -m pip install -r /temp/requirements.txt


EXPOSE 8888

#CMD python run_keras_server.py
