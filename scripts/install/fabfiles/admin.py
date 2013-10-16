from fabric.api import run, local
from fabric.operations import put

import util.awsconnector as aws
from util.config_manager import set_local, get_local, config_path

import os

execute = run

def dependencies(role):
    put('dependencies/{0}.sh'.format(role), '.')

    execute('chmod +x ~/{0}.sh; ~/{0}.sh; rm ~/{0}.sh'.format(role))

def vm(name=None, role='admin'):
    if not name:
        print "Required name for machine!"
        exit(1)

    config  = config_path(role)
    vm_type = get_local(config, 'AWS_INSTANCE_TYPE')
    sec     = get_local(config, 'AWS_SECURITY_GROUP')

    ami_id = get_local(config, 'AWS_AMI_ID')
    if role == 'admin':
        ami_id = os.environ['AWS_AMI_ID']

    instance = aws.launchInstances(
        os.environ['AWS_KEY_PAIR'], vm_type, sec, ami_id, name)

    set_local(config, 'DNS', instance.public_dns_name)
    set_local(config, 'AWS_INSTANCE_ID', instance.id)

    return instance


def ssh():
    #TODO: Code opening console
    pass


def export(name=None, description=None):
    if not name:
        print "Required name for AMI!"
        exit(1)

    if not description:
        print "Required description for AMI!"
        exit(1)

    config = config_path('admin')
    instance_id = get_local(config, 'AWS_INSTANCE_ID')
    ami_id = aws.createAMI(instance_id, name, description)

    set_local(config, 'AWS_AMI_ID', ami_id)


def start():
    config = config_path('admin')
    # may need fix for lists in the future
    instanceIds = [get_local(config, 'AWS_INSTANCE_ID')]
    aws.startInstances(instanceIds)


def stop():
    config = config_path('admin')
    # may need fix for lists in the future
    instanceIds = [get_local(config, 'AWS_INSTANCE_ID')]
    aws.stopInstances(instanceIds)


def terminate():
    config = config_path('admin')
    # may need fix for lists in the future
    instanceIds = [get_local(config, 'AWS_INSTANCE_ID')]
    aws.terminateInstances(instanceIds)
    set_local(config, 'AWS_INSTANCE_ID', '')


def help():
    print '''
    ROLE:
        admin

    ACTIONS:
        help              Show this message
        vm                Creates a VM in AWS and updates the .env files
            name          Name given to the VM
        ssh               Opens remote shell against the VM
        dependencies      Install base dependencies for a given VM role
            role          Selects the role configuration.
        export            Creates an AMI image from the current machine
            name          Name for the AMI image
            description   Description of the AMI image
        start             Starts the VM
        stop              Stops the VM
        terminate         Terminates the VM
        '''
