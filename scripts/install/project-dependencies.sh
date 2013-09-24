#!/bin/bash

sudo yum -y install make glibc-devel gcc gcc-c++ openssl-devel libxml2 libxml2-devel python27-devel mysql-devel
sudo yum -y install mysql mysql-server

sudo /sbin/chkconfig mysqld on
sudo /sbin/service mysqld start

#mysqladmin -u root password 'new-password'
