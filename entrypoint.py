import os
import sys

if os.path.exists("etc/entrypoint/setup_done"):
    print("--- BOOTING ---")
    os.system("service apache2 start")
    os.system("service mysql start")

    setup_done_file = open("etc/entrypoint/setup_done", "r")
    site_name = setup_done_file.read()
    setup_done_file.close()
else:
    print("--- FIRST BOOT ---"+ os.linesep + os.linesep)

    php_versions = ["5.6","7.0","7.1","7.2","7.3","7.4","8.0"]

    # Setting the site name
    site_name = input("What's the domain name of your website ? (without the extension)"+ os.linesep)

    # Setting the PHP Version
    php_versions_strlist = " ".join(php_versions)
    php_v = ""
    while php_v not in php_versions:
        php_v = input(os.linesep +"Which version of PHP do you want to use ? Available versions : "+ php_versions_strlist + os.linesep)

    # Install PHP
    os.system("apt -y install php"+ php_v)
    os.system("apt -y install libapache2-mod-php"+ php_v)
    os.system("apt -y install php"+ php_v +"-cli")
    os.system("apt -y install php"+ php_v +"-gd")
    os.system("apt -y install php"+ php_v +"-intl")
    os.system("apt -y install php"+ php_v +"-memcache")
    os.system("apt -y install php"+ php_v +"-xml")
    os.system("apt -y install php"+ php_v +"-zip")
    os.system("apt -y install php"+ php_v +"-mbstring")
    os.system("apt -y install php"+ php_v +"-mysqli")
    os.system("apt -y install php"+ php_v +"-json")
    os.system("apt -y install php"+ php_v +"-curl")

    # Install MySQL
    os.system("wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb")
    os.system("mv mysql-apt-config_0.8.13-1_all.deb tmp/mysql-apt-config_0.8.13-1_all.deb")
    os.system("dpkg -i /tmp/mysql-apt-config_0.8.13-1_all.deb")
    os.system("apt update -y")
    os.system("apt upgrade -y")
    os.system("apt install -y mariadb-server")
    os.system("service mysql start")

    # Setting MySQL default user
    db_default_user = ""
    while db_default_user.lower() == "root" or len(db_default_user) <= 0:
        db_default_user = input(os.linesep +"Please define the name of the default db user (do not use ROOT) "+ os.linesep)
    db_default_password = ""
    while len(db_default_password) <= 0:
        db_default_password = input(os.linesep +"Please define the password of the default db user"+ os.linesep)

    os.system("mysql -e \"CREATE USER '"+ db_default_user +"'@'localhost' IDENTIFIED BY '"+ db_default_password +"'\"")
    os.system("mysql -e \"GRANT ALL PRIVILEGES ON * . * TO '"+ db_default_user +"'@'localhost'\"")

    # Download PHPMyAdmin
    os.system("mkdir /var/www/phpmyadmin")
    os.system("wget https://files.phpmyadmin.net/phpMyAdmin/5.1.1/phpMyAdmin-5.1.1-all-languages.tar.gz")
    os.system("mv phpMyAdmin-5.1.1-all-languages.tar.gz /tmp/phpMyAdmin-5.1.1-all-languages.tar.gz")
    os.system("cd tmp && tar xvf phpMyAdmin-5.1.1-all-languages.tar.gz")
    os.system("mv /tmp/phpMyAdmin-5.1.1-all-languages/* /var/www/phpmyadmin")

    # Setting HTTP Conf
    default_config_file = open("/etc/apache2/sites-available/000-default.conf", "r")
    defaut_config_content = default_config_file.read()
    default_config_file.close()

    defaut_config_content = defaut_config_content.replace("#ServerName www.example.com","ServerName "+ site_name +".local")
    default_config_file = open("/etc/apache2/sites-available/000-default.conf", "w")
    default_config_file.write(defaut_config_content)
    default_config_file.close()

    phpmya_config_content = defaut_config_content.replace("ServerName web-project.local","ServerName phpmyadmin.local")
    phpmya_config_content = phpmya_config_content.replace("/var/www/html","/var/www/phpmyadmin")
    phpmya_config_file = open("/etc/apache2/sites-available/phpmyadmin-default.conf", "w")
    phpmya_config_file.write(phpmya_config_content)
    phpmya_config_file.close()
    os.system("ln -s /etc/apache2/sites-available/phpmyadmin-default.conf /etc/apache2/sites-enabled/phpmyadmin-default.conf")

    # Setting directory access rights
    os.system("chown www-data:www-data /var/www/html")
    os.system("chown www-data:www-data /var/www/phpmyadmin")
    os.system("mkdir /tmp/php")
    os.system("chown www-data:www-data /tmp/php")

    # Clean up
    os.system("rm mysql-apt-config_0.8.13-1_all.deb")

    # First boot done
    print("End of FIRST BOOT, the lamp server is ready.")
    setup_done_file = open("etc/entrypoint/setup_done", "w")
    setup_done_file.write(site_name)
    setup_done_file.close()
    os.system("service apache2 start")

print("Your website should be accessible at the following adress : "+ site_name +".local")
print("PHPMyAdmin should be accessible at the following adress : phpmyadmin.local")
os.system("bash")