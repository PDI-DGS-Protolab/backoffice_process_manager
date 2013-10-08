import os
from util.awsconnector import launchInstances, download, upload
from util.config_manager import get_local, set_local
from fabric.api import run, local

execute = run


CONFIG_FILE = 'config/db.env'


def vm():
    ami_id = get_local(CONFIG_FILE, 'AWS_AMI_ID')
    type = get_local(CONFIG_FILE, 'AWS_INSTANCE_TYPE')
    sec = get_local(CONFIG_FILE, 'AWS_SECURITY_GROUP')

    instance = launchInstances(
        os.environ['AWS_KEY_PAIR'], type, sec, ami_id)

    download('.env', '.env')
    set_local('.env', 'DB_HOST', instance.public_dns_name)
    upload('.env', '.env')
    os.remove('.env')

    set_local(CONFIG_FILE, 'DNS', instance.public_dns_name)
    set_local(CONFIG_FILE, 'AWS_INSTANCE_ID', instance.id)


def install():
    execute('''
        sudo yum -y install mysql mysql-server
        sudo /sbin/chkconfig mysqld on
        sudo /sbin/service mysqld start
        ''')


def sync():
    execute('''
        source ~/cli.env
        cd "$REPO_NAME"
        source venv/bin/activate
        cd "$REPO_NAME"
        ./manage.py syncdb
        ''')


def help():
    print '''
    ROLE:
        db

    ACTIONS:
        help            Show this message
        vm              Creates a VM in AWS and updates the .env files
        install         Install the base dependencies for the database
        sync            Synchronize the database
    '''
