#!/bin/bash

sudo yum -y install mysql mysql-server

sudo /sbin/chkconfig mysqld on
sudo /sbin/service mysqld start

#mysqladmin -u root password 'new-password'