# LAMP-setup
Small script for set a LAMP server on a Debian machine. This will install Apache, PHP and MySQL on a light Debian server from Docker hub.

## HOW TO USE

### First step, download a Debian 10 image from Docker Hub.

`docker pull debian:10`

### Second step, create you container
[PROJECT NAME] => Name of you project
[LOCAL FOLDER] => Path of your local folder shared with the container

`docker run -it --name [PROJECT NAME] -v [LOCAL FOLDER]:/var/www/html -p 80:80 debian:10`

### Third step, execute the LAMP installation
Once your container is started and you terminal is logged to the shell of the virtual machine, you can
download the following files : "lamp.sh" and "virtualhost.py" from this repository, and paste these files at the root of your local folder.

After that, execute `bash /var/www/html/lamp.sh`

Let the process run... till you'll need to provide some anwser during the MySQL installation.
You can keep the default configuration, or edit the configuration by reading the instruction.

### Final step
Open the "hosts" file of you local systeme.
The path depends on your system, for Windows computer, you can find it here : C:\Windows\System32\drivers\etc\hosts

Then add the following lines, save and close :

`127.0.0.1 phpmyadmin.local`

`127.0.0.1 [DOMAIN NAME].local`

The [DOMAIN NAME] is the string that you've provide at the question "What's the domain name of your website ? (without the extension)"

Now, you just have to delete the files "lamp.sh" and "virtualhost.py", and add an "index.php" file into the root of you local folder.

Call [DOMAIN NAME].local in you favorite web browser... it should work !

### TO DO
This script is not perfect... and there're still things to do !
* find how to set an autostart for the services : Apache2 and MySQL
* adding a process to set up an SSL layer and an SMTP service
