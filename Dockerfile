FROM phusion/baseimage:0.9.11

ENV HOME /root

RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

CMD ["/sbin/my_init"]

RUN apt-get update

RUN apt-get install -y build-essential libssl-dev

# The build tools use Git and SVN to get the source code for the languages
RUN apt-get install -y git subversion

# We'll put all of our languages here in this main directory
RUN mkdir -p /lang/ruby /lang/python /lang/node

RUN cd /tmp; git clone https://github.com/sstephenson/ruby-build.git; cd ruby-build; ./install.sh
RUN cd /tmp; git clone https://github.com/yyuu/pyenv.git; cd pyenv/plugins/python-build; ./install.sh
RUN cd /tmp; git clone https://github.com/creationix/nvm.git; cd nvm; NVM_DIR=/lang/node ./install.sh

# Ruby versions
RUN apt-get install -y autoconf bison zlib1g-dev
RUN ruby-build 1.8.7-p375 /lang/ruby/1.8.7-p375
RUN ruby-build 1.9.3-p545 /lang/ruby/1.9.3-p545
RUN ruby-build 2.0.0-p451 /lang/ruby/2.0.0-p451
RUN ruby-build 2.1.0 /lang/ruby/2.1.0

# Python versions
RUN apt-get install -y libreadline-dev libbz2-dev libsqlite3-dev
RUN python-build 2.6.9 /lang/python/2.6.9
RUN python-build 2.7.8 /lang/python/2.7.8
RUN python-build 3.1.5 /lang/python/3.1.5
RUN python-build 3.2.5 /lang/python/3.2.5
RUN python-build 3.3.5 /lang/python/3.3.5
RUN python-build 3.4.1 /lang/python/3.4.1

# Node.js versions
RUN /bin/bash -c 'source /lang/node/nvm.sh && nvm install v0.9.12'
RUN /bin/bash -c 'source /lang/node/nvm.sh && nvm install v0.10.29'
RUN /bin/bash -c 'source /lang/node/nvm.sh && nvm install v0.11.13'
RUN cd /lang/node; rm -rf bin current test
RUN cd /lang/node; git ls-files | xargs rm -rf 2>/dev/null || exit 0
RUN cd /lang/node; rm -rf .git

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
