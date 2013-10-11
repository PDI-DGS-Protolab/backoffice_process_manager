import boto.ec2
import boto.s3
import time
import os

config = os.environ


###############################################################################
#####                           EC2 Utilities                             #####
###############################################################################
def connectec2():
    conn = boto.ec2.connect_to_region(
        config['AWS_REGION'],
        aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    if not conn:
        print('Connection error')
    else:
        return conn


def launchInstances(keyName, instanceType, securityGroups, ami_id, instance_name=None):

    print keyName
    print instanceType
    print securityGroups
    print ami_id

    conn = connectec2()
    reservation = conn.run_instances(
        ami_id,
        min_count=1,
        max_count=1,
        key_name=keyName,
        instance_type=instanceType,
        security_groups=[securityGroups])
    instance = reservation.instances[0]
    
    if instance_name:
        conn.create_tags([instance.id], {"Name": instance_name})
    
    print('Waiting for instance to start...')
    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        time.sleep(10)
        status = instance.update()
    if status == 'running':
        print('New instance "' + instance.id +
              '" accessible at ' + instance.public_dns_name)
        return instance
    else:
        print('Instance status: ' + status)
        return


def startInstances(instaceIds):
    conn = connectec2()
    return conn.start_instances(
        instance_ids=instaceIds)


def stopInstances(instaceIds, force=False):
    conn = connectec2()
    return conn.stop_instances(
        instance_ids=instaceIds,
        force=force)


def terminateInstances(instaceIds):
    conn = connectec2()
    return conn.terminate_instances(
        instance_ids=instaceIds)


def createAMI(instanceId, name=None, description=None):
    conn = connectec2()
    return conn.create_image(
        instanceId, 
        name=name, 
        description=description)


###############################################################################
#####                            S3 Utilities                             #####
###############################################################################
def connects3():
    conn = boto.connect_s3(config['AWS_ACCESS_KEY_ID'],
                           config['AWS_SECRET_ACCESS_KEY'])

    if not conn:
        print('Connection error')
    else:
        return conn


def download(keyName, fileName):
    conn = connects3()
    bucket_name = config['BUCKET_NAME']
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(keyName)
    key.get_contents_to_filename(fileName)


def upload(keyName, fileName):
    conn = connects3()
    bucket_name = config['BUCKET_NAME']
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(keyName)
    key.set_contents_from_filename(fileName, replace=True)
    key.make_public()
