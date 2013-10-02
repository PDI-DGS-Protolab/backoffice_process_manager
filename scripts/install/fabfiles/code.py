import os
from fabric.api import run, local
from fabric.operations import put

from util.awsconnector import launchInstances
from util.config_manager import set_local, get_local

execute = run

CONFIG_FILE = 'config/code.env'


def vm():
    ami_id = get_local(CONFIG_FILE, 'AWS_AMI_ID')
    type = get_local(CONFIG_FILE, 'AWS_INSTANCE_TYPE')
    sec = get_local(CONFIG_FILE, 'AWS_SECURITY_GROUP')

    instance = launchInstances(os.environ['AWS_KEY_PAIR'], type, sec, ami_id)

    set_local(CONFIG_FILE, 'DNS', instance.public_dns_name)
    set_local(CONFIG_FILE, 'AWS_INSTANCE_ID', instance.id)


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
