import os
from fabric.api import run, local


from util.awsconnector import launchInstances, createAMI, download, upload
from util.config_manager import set_local, get_local
import admin

execute = run


def vm(name=None):
    instance = admin.vm(name=name, role='db')

    download('.env', '.env')
    set_local('.env', 'DB_HOST', instance.public_dns_name)
    upload('.env', '.env')
    os.remove('.env')

def sync():
    execute('''
        source ~/cli.env
        cd "$REPO_NAME"
        source venv/bin/activate
        cd "$REPO_NAME"
        ./manage.py syncdb
        ''')

def init(dbName, username, password, host="*"):
    createDb(dbName)
    createUser(username, password, dbName)
    authorize(username, host, dbName)

def createDb(dbName):
    execute('mysql -u root -p -e "CREATE DATABASE {0};'.format(dbName))


def createUser(username, password, dbName):
    execute("""mysql -u root -e "CREATE USER '{0}'@'localhost' IDENTIFIED BY '{1}';" """.format(username, password))
    authorize(username, "localhost", dbName)


def authorize(username, hostname, dbName=None):
    if dbName:
        execute("""mysql -u root -p -e "GRANT ALL PRIVILEGES ON {0}.* TO '{1}'@'{2}';" """.format(dbName, username, hostname))
    else:
        execute("""mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO '{1}'@'{2}';" """.format(username, hostname))


def help():
    print '''
    ROLE:
        db

    ACTIONS:
        help            Show this message
        vm              Creates a VM in AWS and updates the .env files. Arguments: 1 optional
            name        Name given to the VM
        sync            Synchronize the database
        init            Creates a database, user and grants privileges
        createDb        Creates a database
        createUser      Creates a user
        authorize       Authorizes a user from a host to access a database
        '''
