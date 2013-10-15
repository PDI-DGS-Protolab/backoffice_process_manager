#!/bin/bash

sudo yum -y install make glibc-devel gcc gcc-c++ openssl-devel libxml2 libxml2-devel python27-devel mysql-devel mysql httpd

sudo chkconfig httpd on
sudo /etc/init.d/httpd start
