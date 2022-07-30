# LAMP-Server
Small script for set a LAMP server on a Debian machine. This will install Apache, PHP and MySQL on a light Debian server from Docker hub.

## HOW TO USE

This script is made for to be used with [Docker](https://www.docker.com/).

### First step, Download the src files from this repository
Put these 3 files : "Dockerfile", "lamp-start.sh" and "virtualhost.py" into a folder.

[BUILD FOLDER] => The path of the folder where you put the 3 files

Them, build the docker image
`cd [BUILD FOLDER]`
`docker build -t lamp .`

### Second step, create your container
[PROJECT NAME] => Name of you project
[LOCAL FOLDER] => Path of your local folder shared with the container

`docker run -it --name [PROJECT NAME] -v [LOCAL FOLDER]:/var/www/html -p 80:80 lamp:latest`

### Third step, execute the LAMP installation
Once your container is started for the time, a setup script will be lauched.

Select the PHP version, provide the name of your website... and let the process run...
till you'll need to provide some anwser during the MySQL installation.
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
* adding a process to set up an SSL layer and an SMTP service
