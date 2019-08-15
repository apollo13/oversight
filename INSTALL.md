# Installation guide
This guide is written to be used with a raspbian.

## Setup network
Set a static IP adress in '/etc/dhcpcd.conf'

```
sudo -i
echo "interface eth0" >> /etc/dhcpcd.conf
echo "static ip_address=10.2.3.4/24" >> /etc/dhcpcd.conf
echo "static routers=10.2.3.1" >> /etc/dhcpcd.conf
echo "static domain_name_server=10.2.3.2 10.2.3.3" >> /etc/dhcpcd.conf
reboot 
```

## Setup SSH(optional, but handy)
Edit /etc/ssh/sshd_config to fit your needs
```
sudo vim /etc/ssh/sshd_config
```
Start and enable ssh
```
sudo systemctl enable --now ssh
```
## Install oversight
Install poetry
```
sudo pip3 install poetry
```
Create a user
```
sudo adduser --system oversight
```
Change to the overside user
```
sudo su - oversight -s /bin/bash
```
Go to the home directory
```
cd /home/oversight
```
Clone the oversight git repo
```
git clone https://github.com/feanor12/oversight.git
```
Change working directory to the cloned repository
```
cd oversight
```
Checkout the django2 branch
```
git checkout django2
```
Install dependencies
```
poetry install
```
Prepare config file
```
cp -r example/ config
vim config/settings.py
```
Generate Database, Superuser and static files
```
poetry shell
env PYTHONPATH="./config" ./manage.py migrate –settings="settings"
env PYTHONPATH="./config" ./manage.py collectstatic –settings="settings"
env PYTHONPATH="./config" ./manage.py createsuperuser –settings="settings"
```
Test server
```
env PYTHONPATH=“./config” ./manage.py runserver –settings="settings"
firefox http://127.0.0.1:8000
```

## Install Proxy
Install nginx
```
sudo apt install nginx
```
Copy template from oversight
```
sudo cp /home/oversight/oversight/ansible/roles/nginx/templates/nginx.conf /etc/nginx/nginx.conf
```
Replace the placeholders in the template and remove template if-lines
```
sudo sed -i -e "s/inventory_hostname/my.domain.com/g" /etc/nginx/nginx.conf
sudo sed -i -e "s/{{ 443 if nginx_no_ssl is undefined else 80 }}/443/g" /etc/nginx/nginx.conf
sudo sed -i -e "/{%.*%}/d" /etc/nginx/nginx.conf
```
Copy ssl certificates
```
sudo mkdir /etc/nginx/ssl
sudo cp server.crt server.key dhparams.pem /etc/nginx/etc
```

TODO
 -  fix server.py 
 - start services 
 - copy systemd unit files 
 - start services(systemctl)
