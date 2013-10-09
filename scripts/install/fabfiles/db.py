import os
from util.awsconnector import launchInstances, download, upload
from fabric.api import run, local

execute = run
CONFIG_FILE = 'config/db.env'


def vm():
    type = get_local(CONFIG_FILE, 'INSTANCE_TYPE')
    instance = launchInstances(
        os.environ['AWS_KEY_PAIR'], type)

    download('.env', '.env')
    set_local('.env', 'DB_HOST', instance.public_dns_name)
    upload('.env', '.env')
    os.remove('.env')

    set_local(CONFIG_FILE, 'DNS', instance.public_dns_name)
    set_local(CONFIG_FILE, 'AWS_INSTANCE_ID', instance.id)


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
    execute("""mysql -u root -p -e "CREATE USER '""" + username + """'@'localhost' IDENTIFIED BY '""" + password + """';" """)


def authorize(username, hostname, dbName=None):
    if dbName:
        execute("""mysql -u root -p -e "GRANT ALL PRIVILEGES ON """ + dbName + """.* TO '""" + username + """'@'""" + hostname + """';" """)
    else:
        execute("""mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO '""" + username + """'@'""" + hostname + """';" """)

def help():
    print '''ROLE:
        db

    ACTIONS:
        help            Show this message
        vm              Creates a VM in AWS and updates the .env files
        sync            Synchronize the database
        init            Creates a database, user and grants privileges
        createDb        Creates a database
        createUser      Creates a user
        authorize       Authorizes a user from a host to access a database
        '''
