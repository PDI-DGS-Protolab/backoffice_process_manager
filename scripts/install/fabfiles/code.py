import os
from fabric.api import run, local
from fabric.operations import put

from util.awsconnector import launchInstances, createAMI
from util.config_manager import set_local, get_local
import admin

execute = run


def vm(name=None):
    instance = admin.vm(name=name, role='code')


def ssh():
    #TODO: Code opening console
    pass


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
        pip install -r requirements.txt
        wget --output-document .env $AWS_URL
        python manage.py collectstatic --noinput
        ''')

def syncdb():
    execute('''
        source ~/cli.env
        cd "$REPO_NAME"
        source venv/bin/activate
        cd "$REPO_NAME"
        wget --output-document .env $AWS_URL
        source .env
        ./manage.py syncdb --noinput
        ''')

def run():
    print execute('''
    source ~/cli.env
    cd "$REPO_NAME"
    source venv/bin/activate
    cd "$REPO_NAME"

    wget --output-document .env $AWS_URL

    nohup foreman start -e .env &>out.log &
    exit
    ''', pty=False)


def logs():
    print execute('''
    source ~/cli.env
    cd "$REPO_NAME"/"$REPO_NAME"
    tail -f out.log
    ''')


def stop():
    print execute('''
        killall -9 foreman
        killall -9 gunicorn
        killall -9 python
        ''')


def help():
    print '''
    ROLE:
        code

    ACTIONS:
        help            Shows this message
        vm              Creates a VM in AWS and updates the .env files
            name        Name given to the VM
        ssh             Opens remote shell against the VM
        clone           Clones the repository and switches to the current branch
        update          Updates the code in the current branch and the requirements if necessary
        syncdb          Create database model
        run             Starts the service saving the generated logs in a file
        logs            Shows the output logs generated in the ejecution of the service
        stop            Stops the service
    '''
