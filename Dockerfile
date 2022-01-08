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

# Prepare PHP installation
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
RUN echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list
RUN apt update
RUN apt upgrade -y

RUN apt update
RUN apt full-upgrade -y
RUN mkdir /etc/entrypoint
COPY virtualhost.py /tmp/virtualhost.py
COPY lamp-start.sh /etc/entrypoint/lamp-start.sh
ENTRYPOINT bash /etc/entrypoint/lamp-start.sh
