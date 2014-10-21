FROM {{ dockerfile.from }}

RUN apt-get update

RUN apt-get -y install git python-pip

RUN cd /tmp; git clone https://github.com/robmadole/jig.git --branch {{ jig.rev }}

RUN /usr/bin/pip2 install /tmp/jig
