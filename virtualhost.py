#!/usr/bin/python
import sys

# -- Set the website Virtualhost
website = sys.argv[1]
website_local_conf_file = open(website +".local.conf")
file_content = website_local_conf_file.read()
website_local_conf_file.close()

server_admin_str_replace = "ServerAdmin webmaster@"+ website +".local\n\tServerName "+ website +".local\n\tServerAlias www."+ website +".local"

website_local_conf_file = open(website +".local.conf","w")
file_content = file_content.replace("ServerAdmin webmaster@localhost", server_admin_str_replace)
website_local_conf_file.write(file_content)

website_local_conf_file.close()

# -- Set the PhpMyAdmin Virtualhost
phpmyadmin_local_conf_file = open("phpmyadmin.local.conf")
file_content = phpmyadmin_local_conf_file.read()
phpmyadmin_local_conf_file.close()

server_admin_str_replace = "ServerAdmin webmaster@phpmyadmin.local\n\tServerName phpmyadmin.local\n\tServerAlias www.phpmyadmin.local"

phpmyadmin_local_conf_file = open("phpmyadmin.local.conf","w")
file_content = file_content.replace("ServerAdmin webmaster@localhost", server_admin_str_replace)
file_content = file_content.replace("DocumentRoot /var/www/html","DocumentRoot /var/www/phpmyadmin")
phpmyadmin_local_conf_file.write(file_content)

phpmyadmin_local_conf_file.close()