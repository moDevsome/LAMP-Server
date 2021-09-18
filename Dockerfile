FROM debian:10
COPY lamp-start.sh /etc/lamp/lamp-start.sh
COPY virtualhost.py /etc/lamp/virtualhost.py
ENTRYPOINT bash /etc/lamp/lamp-start.sh