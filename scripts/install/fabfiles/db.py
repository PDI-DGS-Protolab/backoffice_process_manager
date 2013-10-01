import os
from utils.awsconnector import launchInstances, download, upload
from fabric.api import run, local

execute = run

import os
from util.awsconnector import launchInstances, download, upload

def vm():
    config = open("config/cli.env",'r')
    env = config.readlines()
    config.close()
    for var in env:
        if not (var == ""):
            keyVal = var.split("=")
            os.environ[keyVal[0]] = keyVal[1][0:-1]
    instance = launchInstances(os.environ['AWS_KEY'],os.environ['INSTANCE_TYPE'])
    
    download('.env', '.env')
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if 'DB_HOST' in lines[i]:
            lines[i] = 'DB_HOST=' + instance.public_dns_name + '\n'
    
    with open('.env', 'w') as f:
        f.writelines(lines)
    
    upload('.env','.env')
    os.remove('.env')

    # Needs beautify
    with open('config/cli.env', 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if 'DB_HOST' in lines[i]:
            lines[i] = 'DB_HOST=' + instance.public_dns_name + '\n'
    
    with open('config/cli.env', 'w') as f:
        f.writelines(lines)

def sync():
    execute('''
        source ~/cli.env
        cd "$REPO_NAME"
        source venv/bin/activate
        cd "$REPO_NAME"
        ./manage.py syncdb
        ''')

