sudo apt-get update
sudo apt-get install apache2
sudo apt-get install mysql-server php5-mysql
sudo mysql_install_db
sudo mysql_secure_installation
sudo apt-get install php5 libapache2-mod-php5 php5-mcrypt php5-gd php5-curl php5-cli
sed -i -e "s/index.html index.cgi index.pl index.php/index.php index.html index.cgi index.pl/" /etc/apache2/mods-enabled/dir.conf
sudo service apache2 restart
sudo apt-get install php5-cli
echo "<?php phpinfo();" > /var/www/html/info.php