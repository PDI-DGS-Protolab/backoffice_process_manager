#! /usr/bin/python

from os import listdir, environ
from os.path import expanduser
from sys import exit

from fabric.context_managers import settings
from fabric.api import env

from util.config_manager import get_local, load_into_os_environment, check_locals

import re
import importlib
import argparse


fabfilesPath = "./fabfiles"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "role", help="Role that will perform the action")
    parser.add_argument(
        "action", help="Action to perform", nargs='*')
    parser.add_argument(
        "-vm", help="Creates a virtual machine USE WITH CARE", action="store_true")

    args = parser.parse_args()

    fabfiles = [f for f in listdir(fabfilesPath) if re.match(r'^.+\.py$', f)]

    for f in fabfiles:
        f = f.split('.')[0]
        if args.role == f:
            role = f

    if not role:
        print "Invalid role"
        exit(1)

    action = args.action[0] # we need to separate the action from its arguments
    arguments = args.action[1:]

    url = None
    if action != 'help':
        # Reading role configuration file
        user = get_local('config/{0}.env'.format(role), 'USER')
        dns = get_local('config/{0}.env'.format(role), 'DNS')

        if not user:
            print 'USER variable not set'
            exit(1)

        if not dns and action != 'vm':
            print 'Create a VM first'
            exit(1)

        # Reading cli configuration file and adding it to the process
        # environment
        check_locals('config/cli.env')
        load_into_os_environment('config/cli.env')

    makeCall(role, action, arguments, user, dns)

    print '''
    ---------------------
          SUCCESS!
    ---------------------
        '''

def makeCall(role, action, arguments=None, user=None, dns=None):
    fabfile = importlib.import_module('fabfiles.' + role, role)

    pem = None
    if action != 'help':
        pem = expanduser(environ['PEM'])

    url = user + '@' + dns
    with settings(host_string=url, key_filename=pem):
        getattr(fabfile, action)(*arguments)

    # CORRECT FOR THE CASE OF A NEW VM
    print('Finished work at ' + dns)

main()
