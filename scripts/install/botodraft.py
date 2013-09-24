import fabric
import boto.ec2
import re
import time

config = {}


def read_env(path):
    try:
        with open(path) as f:
            content = f.read()
    except IOError, e:
        content = ''
        print e

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            # os.environ.setdefault(key, val)
            config[key] = val


def connect ():
    conn = boto.ec2.connect_to_region(
        'us-west-2',
        aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    if not conn:
        print ('Connection error')
    else: 
        return conn


def launchInstances ( keyName, instanceType, securityGroups ):
    conn = connect()
    reservation = conn.run_instances(
        config['AWS_AMI_ID'],
        min_count=1,
        max_count=1,
        key_name=keyName,
        instance_type=instanceType,
        security_groups=securityGroups )
    instance = reservation.instances[0]
    print('Waiting for instance to start...')
    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        time.sleep(10)
        status = instance.update()
    if status == 'running':
        print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name)
        return instance
    else:
        print('Instance status: ' + status)
        return

def startInstances ( instaceIds ):
    conn = connect()
    return conn.start_instances(
        instance_ids=instaceIds )


def stopInstances ( instaceIds, force=False ):
    conn = connect()
    return conn.stop_instances(
        instance_ids=instaceIds,
        force=force )

 
def terminateInstances ( instaceIds ):
    conn = connect()
    return conn.terminate_instances(
        instance_ids=instaceIds )

read_env('config/cli.env')
launchInstances( 'protolab2', 't1.micro', None)
