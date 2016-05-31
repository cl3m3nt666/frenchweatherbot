FROM debian
MAINTAINER cl3m3nt
RUN apt-get update
RUN apt-get -y install python wget
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN export LC_ALL='en_US.utf8'
COPY frenchweatherbot /frenchweatherbot
WORKDIR /frenchweatherbot
RUN pip install -r requirements.txt
CMD ["bash", "runbot.sh"]
