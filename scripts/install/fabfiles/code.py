import os, sys
from fabric.api import run,local
from fabric.operations import put
from util.awsconnector import launchInstances

execute = run

def vm():
    config = open("config/cli.env",'r')
    env = config.readlines()
    config.close()
    for var in env:
        if not (var == ""):
            keyVal = var.split("=")
            os.environ[keyVal[0]] = keyVal[1][0:-1]

    instance = launchInstances(os.environ['AWS_KEY'],os.environ['INSTANCE_TYPE'])

    with open('config/cli.env', 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if 'CODE_HOST' in lines[i]:
            lines[i] = 'CODE_HOST=' + instance.public_dns_name + '\n'
    
    with open('config/cli.env', 'w') as f:
        f.writelines(lines)

def install_base():

    put('dependencies/base.sh', '.')

    execute('chmod +x ~/base.sh; ~/base.sh; rm ~/base.sh')

def clone():
    put('config/cli.env', '.')

    execute('''
        source ~/cli.env
        mkdir "$REPO_NAME"
        cd $REPO_NAME
        virtualenv -p $PYTHON_PATH venv --distribute
        source venv/bin/activate
        git clone $REPO_URL "$REPO_NAME"
        cd "$REPO_NAME"
        git checkout $BRANCH
        ''')

def update():
    execute('''
        source ~/cli.env
        cd "$REPO_NAME"
        source venv/bin/activate

        cd "$REPO_NAME"
        git pull origin $BRANCH
        sh ./scripts/install/dependencies/code.sh
        pip install -r requirements.txt
        wget --output-document .env $AWS_URL
        python manage.py collectstatic --noinput
        ''')

def run():
    execute('''
    source ~/cli.env
    cd "$REPO_NAME"
    source venv/bin/activate
    cd "$REPO_NAME"

    wget --output-document .env $AWS_URL

    nohup foreman start -e .env &>out.log &
    exit
    ''', pty=False)

def logs():
    execute('''
    source ~/cli.env
    cd "$REPO_NAME"/"$REPO_NAME"
    tail -f out.log
    ''')

def stop():
    execute('''
        killall -9 foreman
        killall -9 gunicorn
        killall -9 python
        ''')