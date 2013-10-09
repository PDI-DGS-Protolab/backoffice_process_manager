import os
from fabric.api import run, local
from fabric.operations import put

from util.awsconnector import launchInstances, createAMI
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


def create_ami(name=None, description=None):
    instance_id = get_local(CONFIG_FILE, 'AWS_INSTANCE_ID')
    ami_id = createAMI(instance_id, name, description)


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
        create_ami      Creates an AMI image from the current machine. Accepts 2 optional arguments
            name        Name for the AMI image
            description Description of the AMI image
        clone           Clones the repository and switches to the current branch
        update          Updates the code in the current branch and the requirements if necessary
        run             Starts the service saving the generated logs in a file
        logs            Shows the output logs generated in the ejecution of the service
        stop            Stops the service
    '''
