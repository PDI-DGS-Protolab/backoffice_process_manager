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

def init(dbName, username, password, host="%"):
    createDb(dbName, password)
    createUser(username, password)
    authorize(username, host, password, dbName)

def createDb(dbName, password):
    execute('mysql -uroot --password={1} -e "CREATE DATABASE {0};" '.format(dbName, password))


def createUser(username, password):
    execute("""mysql -uroot --password={1} -e "CREATE USER '{0}' IDENTIFIED BY '{1}';" """.format(username, password))


def authorize(username, hostname, password, dbName=None):
    if dbName:
        execute("""mysql -u root --password={3} -e "GRANT ALL PRIVILEGES ON {0}.* TO '{1}'@'{2}';" """.format(
            dbName, username, hostname, password))
    else:
        execute("""mysql -u root --password={2} -e "GRANT ALL PRIVILEGES ON *.* TO '{0}'@'{1}';" """.format(
            username, hostname, password))


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
