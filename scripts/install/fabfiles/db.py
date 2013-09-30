import os
from utils.awsconnector import launchInstances, download, upload
from fabric.api import run, local

execute = run

def vm():
    config = open("config/cli.env",'r')
    env = readlines(config)
    config.close()
    for var in env:
        keyVal = split(var,"=")
        os.environ[keyVal[0]] = keyVal[1]
    instance = launchInstances(os.environ[AWS_KEY],os.environ[INSTANCE_TYPE],os.environ[SECURITY_GROUP])
    download('.env', '.env')
    f = open('.env', 'w')
    for line in f:
        if 'DB_HOST' in line:
            line=line.replace(line,'DB_HOST=' + instance.public_dns_name)
    f.close()
    upload('.env','.env')
    os.remove('.env')

def sync():
    execute('''
        source ~/cli.env
        cd "$REPO_NAME"
        source venv/bin/activate
        cd "$REPO_NAME"
        ./manage.py syncdb
        ''')

