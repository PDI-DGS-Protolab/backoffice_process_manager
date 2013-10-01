import fabric
import boto.ec2, boto.s3
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


def connectec2 ():
    conn = boto.ec2.connect_to_region(
        'us-west-2',
        aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    if not conn:
        print ('Connection error')
    else: 
        return conn


def connects3 ():
    conn = boto.connect_s3(config['AWS_ACCESS_KEY_ID'], config['AWS_SECRET_ACCESS_KEY'])

    if not conn:
        print ('Connection error')
    else: 
        return conn


def launchInstances ( keyName, instanceType, securityGroups=None ):
    conn = connectec2()
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
    conn = connectec2()
    return conn.start_instances(
        instance_ids=instaceIds )


def stopInstances ( instaceIds, force=False ):
    conn = connectec2()
    return conn.stop_instances(
        instance_ids=instaceIds,
        force=force )

 
def terminateInstances ( instaceIds ):
    conn = connectec2()
    return conn.terminate_instances(
        instance_ids=instaceIds )


def download ( keyName, fileName ):
    conn = connects3()
    bucket_name = config['BUCKET_NAME']
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(keyName)
    key.get_contents_to_filename(fileName)

def upload ( keyName, fileName ):
    conn = connects3()
    bucket_name = config['BUCKET_NAME']
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(keyName)
    key.set_contents_from_filename(fileName, replace=true)
    key.make_public()


read_env('config/cli.env')
