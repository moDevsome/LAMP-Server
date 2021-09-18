if [[ -f "/etc/lamp/setup_done" ]]; then
    echo "---- LAMP SERVER IS STARTING ----"
    service apache2 start

    echo "Want you start the MySQL service ? Press y/Y or just ENTER"
    read mysql_start
    if [[ "${mysql_start^^}" == "Y" ]]; then

        # if the lock file is still present, we need to delete it, else mySQL could not start
        if [[ -f "/var/run/mysqld/mysqld.sock.lock" ]]; then
            rm /var/run/mysqld/mysqld.sock.lock
        fi

        service mysql start
    fi
else
    echo "---- ----------------------------- ----"
    echo "---- LAMP SETUP SCRIPT IS STARTING ----"
    echo "---- ----------------------------- ----"
    echo " "

    echo "Which version of PHP do you want to use ? Available versions : 5.6 7.0 7.1 7.2 7.3 7.4 8.0"
    read php_version
    php_versions_list="5.6 7.0 7.1 7.2 7.3 7.4 8.0"
    selected_php_version=""
    while [ "$selected_php_version" == "" ]
    do
        for v in $php_versions_list
        do
            if [[ $v == "$php_version" ]]; then
                selected_php_version="$php_version"
            fi
        done
        if [[ $selected_php_version == "" ]]; then
            echo "Which version of PHP do you want to use ? Available versions : 5.6 7.0 7.1 7.2 7.3 7.4 8.0"
            read php_version
        fi
    done

    echo "What's the domain name of your website ? (without the extension)"
    read website

    apt update
    apt upgrade -y

    apt -y install lsb-release
    apt -y install apt-transport-https
    apt -y install ca-certificates
    apt -y install wget
    apt update
    apt upgrade -y

    echo " "
    echo "-- Apache --"

    apt -y install apach74e2
    apt update
    apt upgrade -y

    service apache2 start

    a2enmod rewrite
    a2enmod deflate
    a2enmod headers

    service apache2 restart

    echo " "
    echo "-- PHP --"

    wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
    echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list
    apt update
    apt upgrade -y
    apt -y install libapache2-mod-php$selected_php_version
    apt -y install php$selected_php_version-{cli,curl,gd,intl,memcache,mysql,xml,zip,mbstring,json}

    service apache2 restart

    echo " "
    echo "-- MySQL --"
    echo "@see https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-debian-10"
    echo "— Prerequisites"

    apt -y install gnupg
    apt update
    apt upgrade -y

    echo "Step 1 — Adding the MySQL Software Repository"
    cd /tmp
    wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb
    dpkg -i mysql-apt-config*
    apt update
    apt upgrade -y

    echo "Step 2 — Installing MySQL"
    apt -y install mysql-server
    apt update
    apt upgrade -y

    service mysql start

    echo "Step 3 — Securing MySQL"
    mysql_secure_installation

    echo "Step 4 – Testing MySQL"
    mysqladmin -u root -p version

    echo " "
    echo "-- PhpMyAdmin installation AND  Virtualhost setting--"
    wget https://files.phpmyadmin.net/phpMyAdmin/5.1.1/phpMyAdmin-5.1.1-all-languages.tar.gz
    tar xvf phpMyAdmin-5.1.1-all-languages.tar.gz
    mv phpMyAdmin-5.1.1-all-languages /var/www/phpmyadmin
    rm * #assuming that we're always in /tmp dir
    cd /var/www/html
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

    touch /etc/lamp/setup_done
    echo "---- LAMP SETUP SCRIPT IS OVER ----"
fi

echo " "
echo " "
echo "---- LAMP SERVER STATUS ----"
service apache2 status
php -v
service mysql status

## necessary to purchase the startup
bash
