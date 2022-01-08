#!/bin/bash
if [[ -f "/etc/entrypoint/setup_done" ]]; then
    echo "----------------- ------- -----------------"
    echo "                  BOOTING                  "
    echo "----------------- ------- -----------------"
    echo "                                           "
    echo "                                           "
    service apache2 start
    service mysql start
    php -v
else
    echo "----------------- ---------- -----------------"
    echo "                  FIRST BOOT                  "
    echo "----------------- ---------- -----------------"
    echo "                                              "
    echo "                                              "

    echo "What's the domain name of your website ? (without the extension)"
    read website

    # Install PHP
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

    apt -y install php$selected_php_version
    apt -y install libapache2-mod-php$selected_php_version
    apt -y install php$selected_php_version-cli
    apt -y install php$selected_php_version-gd
    apt -y install php$selected_php_version-intl
    apt -y install php$selected_php_version-memcache
    apt -y install php$selected_php_version-xml
    apt -y install php$selected_php_version-zip
    apt -y install php$selected_php_version-mbstring
    apt -y install php$selected_php_version-mysqli
    apt -y install php$selected_php_version-json
    apt -y install php$selected_php_version-curl

    # Install MySQL
    cd /tmp
    wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb
    dpkg -i mysql-apt-config*
    apt update
    apt upgrade -y

    apt -y install mysql-server

    service mysql start
    mysql_secure_installation

    # Import and Unpack PhpMyAdmin
    wget https://files.phpmyadmin.net/phpMyAdmin/5.1.1/phpMyAdmin-5.1.1-all-languages.tar.gz
    tar xvf phpMyAdmin-5.1.1-all-languages.tar.gz
    mv phpMyAdmin-5.1.1-all-languages /var/www/phpmyadmin

    # Managing virtual host config
    cp /etc/apache2/sites-available/000-default.conf $website.local.conf
    cp /etc/apache2/sites-available/000-default.conf phpmyadmin.local.conf
    python3 virtualhost.py $website
    mv $website.local.conf /etc/apache2/sites-available/$website.local.conf
    mv phpmyadmin.local.conf /etc/apache2/sites-available/phpmyadmin.local.conf
    a2ensite $website.local.conf
    a2ensite phpmyadmin.local.conf
    rm *

    cd /var/www
    chown www-data:www-data html
    chown www-data:www-data phpmyadmin

    service apache2 start
    php -v

    touch /etc/entrypoint/setup_done
fi

cd /var/www/html

## necessary to purchase the startup
bash
