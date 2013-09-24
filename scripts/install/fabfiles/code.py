from fabric.api import run,local
from fabric.operations import put


execute = run

def install_base():

    put('../dependencies/base.sh', '.')

    execute('chmod +x ~/base.sh; ~/base.sh; rm ~/base.sh')

def clone():
    put('../config/cli.env', '.')

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