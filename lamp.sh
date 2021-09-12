
echo "---- LAMP SETUP SCRIPT IS STARTING ----"
apt update
apt upgrade -y

echo "-- Apache + PHP"

apt -y install apache2 libapache2-mod-php
apt update
apt upgrade -y

apt -y install php-{curl,gd,intl,memcache,xml,zip,mbstring,json}
service apache2 start

a2enmod rewrite
a2enmod deflate
a2enmod headers

service apache2 restart

apt -y install php php-cli
apt -y install php-{curl,gd,intl,memcache,xml,zip,mbstring,json}
apt -y install php-mysql

service apache2 restart

apt -y install wget
apt update
apt upgrade -y

echo "-- MySQL installation"
echo '@see https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-debian-10'
echo '- Prerequisites'
apt -y install gnupg
apt update
apt upgrade -y

apt -y install lsb-release
apt update
apt upgrade -y

echo 'Step 1 — Adding the MySQL Software Repository'
cd /tmp
wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb
dpkg -i mysql-apt-config*
apt update
apt upgrade -y

echo 'Step 2 — Installing MySQL'
apt -y install mysql-server
apt update
apt upgrade -y

service mysql start

echo 'Step 3 — Securing MySQL'
mysql_secure_installation

echo 'Step 4 – Testing MySQL'
mysqladmin -u root -p version

echo "-- PhpMyAdmin installation + Virtualhost setting"
wget https://files.phpmyadmin.net/phpMyAdmin/5.1.1/phpMyAdmin-5.1.1-all-languages.tar.gz
tar xvf phpMyAdmin-5.1.1-all-languages.tar.gz
mv phpMyAdmin-5.1.1-all-languages /var/www/phpmyadmin
rm * #assuming that we're always in /tmp dir
cd /var/www/html
echo "What's the domain name of your website ? (without the extension)"
read website
cp /etc/apache2/sites-available/000-default.conf $website.local.conf
cp /etc/apache2/sites-available/000-default.conf phpmyadmin.local.conf
python3 virtualhost.py $website
mv $website.local.conf /etc/apache2/sites-available/$website.local.conf
mv phpmyadmin.local.conf /etc/apache2/sites-available/phpmyadmin.local.conf
a2ensite $website.local.conf
a2ensite phpmyadmin.local.conf
service apache2 reload

cd ..
chown www-data:www-data html
chown www-data:www-data phpmyadmin

echo "---- LAMP SETUP SCRIPT IS OVER ----"
service apache2 status
php -v
service mysql status