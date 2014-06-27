FROM phusion/baseimage:0.9.11

ENV HOME /root

RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

CMD ["/sbin/my_init"]

apt-get install -y git

cd /tmp; git clone https://github.com/sstephenson/ruby-build.git; cd ruby-build; ./install.sh

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
