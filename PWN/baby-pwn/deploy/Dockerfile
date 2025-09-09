FROM debian:latest

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m -s /bin/bash brandy

COPY ./xinetd.conf /etc/xinetd.conf
RUN chmod 644 /etc/xinetd.conf

COPY ./just_jump /home/brandy/just_jump
COPY ./gold.txt /home/brandy/gold.txt
COPY ./run.sh /home/brandy/run
COPY ./startchall.sh /usr/bin/startchall
COPY ./xinetd /etc/xinetd.d/xinetd

RUN chown -R root:brandy /home/brandy && chmod -R 550 /home/brandy
RUN chmod 500 /etc/xinetd.d/xinetd && chmod 500 /usr/bin/startchall

CMD ["/usr/bin/startchall"]