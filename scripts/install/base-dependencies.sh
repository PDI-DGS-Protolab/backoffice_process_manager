#/bin/bash

echo  "Installing base platform dependencies!"

yum erase -y ruby rubygems
sudo rm /usr/bin/gem /usr/bin/ruby

sudo yum -y install git python27 python-pip
sudo easy_install virtualenv

sudo ln -s /usr/bin/python-pip /usr/bin/pip

sudo yum -y install ruby19

sudo ln -s /usr/bin/gem1.9 /usr/bin/gem
sudo ln -s /usr/bin/ruby1.9 /usr/bin/ruby

sudo gem install foreman

echo  "Installing security updates!"

sudo yum -y update

echo  "Installation FINISHED!"
