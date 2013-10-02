#! /usr/bin/python

from os import listdir, environ
from os.path import expanduser
from sys import exit

from fabric.context_managers import settings
from fabric.api import env

from util.config_manager import get_local, load_into_os_environment

import re
import importlib
import argparse


fabfilesPath = "./fabfiles"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("role", help="Role that will perform the action")
    parser.add_argument("action", help="Action to perform")
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

    action = args.action

    # Reading role configuration file
    dns = get_local('config/{0}.env'.format(role), 'USER') + \
        '@' + get_local('config/{0}.env'.format(role), 'DNS')

    if not dns and action != 'vm':
        print "Create a VM first"
        exit(1)

    # Reading cli configuration file and adding it to the process environment
    load_into_os_environment('config/cli.env')

    makeCall(role, action, dns)


def makeCall(role, action, dns=None):
    fabfile = importlib.import_module('fabfiles.' + role, role)
    with settings(host_string=dns, key_filename=expanduser(environ['PEM'])):
        getattr(fabfile, action)()

main()
