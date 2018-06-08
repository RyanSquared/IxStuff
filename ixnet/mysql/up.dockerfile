FROM debian:jessie

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y mysql-client mysql-server

ADD ./wait-for-it/wait-for-it.sh /
ADD ./start.sh /

ENTRYPOINT /wait-for-it.sh db:3306 -- /start.sh
