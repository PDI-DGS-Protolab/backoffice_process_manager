import os
from fabric.api import run, local


import util.awsconnector as aws
from util.config_manager import set_local, get_local, config_path

execute = run


def vm(role, name=None):
    config = config_path(role)
    ami_id = get_local(config, 'AWS_AMI_ID')
    type = get_local(config, 'AWS_INSTANCE_TYPE')
    sec = get_local(config, 'AWS_SECURITY_GROUP')

    instance = aws.launchInstances(
        os.environ['AWS_KEY_PAIR'], type, sec, ami_id, name)

    set_local(config, 'DNS', instance.public_dns_name)
    set_local(config, 'AWS_INSTANCE_ID', instance.id)

    return instance


def create_ami(role, name=None, description=None):
    config = config_path(role)
    instance_id = get_local(config, 'AWS_INSTANCE_ID')
    ami_id = aws.createAMI(instance_id, name, description)


def start(role):
    config = config_path(role)
    # may need fix for lists in the future
    instanceIds = [get_local(config, 'AWS_INSTANCE_ID')]
    aws.startInstances(instanceIds)


def stop(role):
    config = config_path(role)
    # may need fix for lists in the future
    instanceIds = [get_local(config, 'AWS_INSTANCE_ID')]
    aws.stopInstances(instanceIds)


def terminate(role):
    config = config_path(role)
    # may need fix for lists in the future
    instanceIds = [get_local(config, 'AWS_INSTANCE_ID')]
    aws.terminateInstances(instanceIds)
    set_local(config, 'AWS_INSTANCE_ID', '')


def help():
    print '''
    ROLE:
        admin

    ACTIONS:
        help            Show this message
        vm              Creates a VM in AWS and updates the .env files. Arguments: 1 positional, 1 optional
            role        Selects the role configuration. AVOID THE USE OF ADMIN ROLE ON THIS FIELD
            name        Name given to the VM
        create_ami      Creates an AMI image from the current machine. Arguments: 1 positional, 2 optional
            role        Selects the role configuration
            name        Name for the AMI image
            description Description of the AMI image
        start           Starts the VM. Arguments: 1 positional
            role        Selects the role configuration
        stop            Stops the VM. Arguments: 1 positional
            role        Selects the role configuration        
        terminate       Terminates the VM. Arguments: 1 positional
            role        Selects the role configuration
        '''
