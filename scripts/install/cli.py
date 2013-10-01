#! /usr/bin/python

import argparse
from os import listdir, system
from subprocess import call
from os.path import join
from sys import exit
import re
from fabric.context_managers import settings
import importlib

fabfilesPath = "./fabfiles"

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("role", help="Role that will perform the action")
    parser.add_argument("action", help="Action to perform")
    parser.add_argument("-vm", help="Creates a virtual machine USE WITH CARE", action="store_true")
    args = parser.parse_args()

    fabfiles = [ f for f in listdir(fabfilesPath) if re.match(r'^.+\.py$', f) ]
    for f in fabfiles:
        f = f.split('.')[0]
        if args.role == f:
            role = f
    if not role:
        print "Invalid role"
        exit(1)

    action = args.action

    if role == "db":
        with open('config/cli.env', 'r') as f:
            lines = f.readlines()
            for l in lines:
                if 'DB_HOST' in l:
                    url = 'ec2-user@' + l.split('=')[1][0:-1]
    elif role == "code":
        with open('config/cli.env', 'r') as f:
            lines = f.readlines()
            for l in lines:
                if 'CODE_HOST' in l:
                    url = 'ec2-user@' + l.split('=')[1][0:-1]

    if args.vm:
        makeCall(role, 'vm')

    makeCall(role, action, url)


def makeCall ( role, action, url=None ):
    # fabcall = 'fab -f ' + join(fabfilesPath, role) + ' ' + action + ' -H ' + url + ' -i ~/.ssh/protolab2.pem'
    # fab -f code.py install_base -H ec2-user@ec2-54-214-198-97.us-west-2.compute.amazonaws.com -i ~/Descargas/protolab2.pem
    # call(fabcall)
    
    fabfile = importlib.import_module('fabfiles.' + role, role)

    with settings(host_string=url, key_filename='~/.ssh/protolab2.pem'):
        getattr(fabfile,action)()

main()