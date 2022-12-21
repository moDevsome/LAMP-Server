# syntax=docker/dockerfile:1
FROM debian:10
RUN apt update
RUN apt full-upgrade -y

# Install basic dependancies
RUN apt -y install lsb-release
RUN apt -y install apt-transport-https
RUN apt -y install ca-certificates
RUN apt -y install wget
RUN apt -y install gnupg
RUN apt -y install vim
RUN apt update
RUN apt upgrade -y

# Install Apache2
RUN apt -y install apache2
RUN apt update
RUN apt upgrade -y
RUN service apache2 start
RUN a2enmod rewrite
RUN a2enmod deflate
RUN a2enmod headers
RUN service apache2 restart

RUN apt update
RUN apt full-upgrade -y
RUN mkdir /etc/entrypoint
COPY entrypoint.py /etc/entrypoint/entrypoint.py
ENTRYPOINT python3 /etc/entrypoint/entrypoint.py