import os
import sys
import json

if os.path.exists("etc/entrypoint/setup_done"):
    print("--- BOOTING ---")
    os.system("service apache2 start")

    setup_done_file = open("etc/entrypoint/setup_done", "r")
    params = json.loads(setup_done_file.read())
    site_name = params["site-name"]
    setup_done_file.close()

    if params["has-mysql"] == "true":
        os.system("service mysql start")
else:
    print("--- Welcome to the FIRST BOOT ! ---"+ os.linesep + os.linesep)
    print("Debian release : "+ os.linesep + os.linesep)
    os.system("lsb_release -a")

    params = {}

    # Setting the site name
    site_name = input("What's the domain name of your website ? (without the extension)"+ os.linesep)
    params["site-name"] = site_name

    # Setting the PHP Version
    php_versions = ["5.6","7.0","7.1","7.2","7.3","7.4","8.0","8.2"]
    php_versions_strlist = " ".join(php_versions)
    php_v = ""
    while php_v not in php_versions:
        php_v = input(os.linesep +"Which version of PHP do you want to use ? Available versions : "+ php_versions_strlist + os.linesep)

    # Prepare PHP installation
    os.system("wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg")
    os.system('echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list')
    os.system("apt update")
    os.system("apt upgrade -y")

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

    # Install Composer
    if input("Do you want to install Composer ? Press \"y\" key to install composer.\n") == "y":
        os.system("wget https://getcomposer.org/installer")
        if os.path.exists("installer"):
            os.replace("installer", "composer-setup.php")

            # Download the installer checksum value
            sha384sum = ""
            checksum_error_message = "\033[0;31m ---ERROR --- \033[0m Composer installer checksum failed."
            os.system("wget https://composer.github.io/installer.sha384sum")
            if os.path.exists("installer.sha384sum"):

                sha384sum_file = open("installer.sha384sum", "r")
                sha384sum_file_content = sha384sum_file.read()
                if len(sha384sum_file_content) > 0:
                    sha384sum = sha384sum_file_content.split()[0]
                else :
                    print(checksum_error_message + " [1]")

            else :
                print(checksum_error_message + " [0]")

            # Check if the installer file sum match with the checksum
            if len(sha384sum) > 0:
                php_cmd = "php -r \"if (hash_file('sha384', 'composer-setup.php') !== 'CHECKSUM') { unlink('composer-setup.php'); }\""
                php_cmd = php_cmd.replace("CHECKSUM", sha384sum)
                os.system(php_cmd)

                if os.path.exists("composer-setup.php"):
                    os.system("php composer-setup.php")
                    os.remove("composer-setup.php")
                else :
                    print(checksum_error_message + " [2]")

                os.remove("installer.sha384sum")

                if os.path.exists("composer.phar"):
                    os.replace("composer.phar", "/usr/local/bin/composer")
                else :
                    print("\033[0;31m ---ERROR --- \033[0m Composer installation failed.")

        else:
            print("\033[0;31m ---ERROR --- \033[0m Download https://getcomposer.org/installer failed")

    # Install MySQL
    if input("Do you want to install MySQL ? Press \"y\" key to install Mysql wich running with mariadb-server.\n") == "y":
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

        # Clean up
        os.system("rm /tmp/mysql-apt-config_0.8.13-1_all.deb")
        os.system("rm /tmp/phpMyAdmin-5.1.1-all-languages.tar.gz")
        os.system("rmdir /tmp/phpMyAdmin-5.1.1-all-languages")

        # Set params dictionnary
        params["has-mysql"] = "true"
    else:
        params["has-mysql"] = "false"

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

    # First boot done
    print("End of FIRST BOOT, the lamp server is ready.")
    setup_done_file = open("etc/entrypoint/setup_done", "w")
    setup_done_file.write(json.dumps(params))
    setup_done_file.close()
    os.system("service apache2 start")

print("Your website should be accessible at the following adress : "+ site_name +".local")

if params["has-mysql"] == "true":
    print("PHPMyAdmin should be accessible at the following adress : phpmyadmin.local")

os.system("bash")