import os
from fabric.api import run, local


from util.awsconnector import launchInstances, createAMI, download, upload
from util.config_manager import set_local, get_local
import admin

execute = run


def vm(name=None):
    instance = admin.vm(role='db', name=name)

    download('.env', '.env')
    set_local('.env', 'DB_HOST', instance.public_dns_name)
    upload('.env', '.env')
    os.remove('.env')


# SACAR NOMBRE DEL FICHERO
def dependencies():
    put('dependencies/db.sh', '.')

    execute('chmod +x ~/db.sh; ~/db.sh; rm ~/db.sh')


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
    execute('mysql -u root -p -e "CREATE DATABASE ' + dbName + '"')


def createUser(username, password, dbName):
    execute("""mysql -u root -p-e "CREATE USER '""" + username +
            """'@'localhost' IDENTIFIED BY '""" + password + """';" """)
    authorize(username, "localhost", dbName)


def authorize(username, hostname, dbName=None):
    if dbName:
        execute("""mysql -u root -p-e "GRANT ALL PRIVILEGES ON """ +
                dbName + """.* TO '""" + username + """'@'""" + hostname + """';" """)
    else:
        execute("""mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO '""" +
                username + """'@'""" + hostname + """';" """)


def help():
    print '''
    ROLE:
        db

    ACTIONS:
        help            Show this message
        vm              Creates a VM in AWS and updates the .env files. Arguments: 1 optional
            name        Name given to the VM
        dependencies    Installs a dependencies script
        sync            Synchronize the database
        init            Creates a database, user and grants privileges
        createDb        Creates a database
        createUser      Creates a user
        authorize       Authorizes a user from a host to access a database
        '''
