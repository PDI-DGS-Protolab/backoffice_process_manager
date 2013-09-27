import os
from utils.awsconnector import launchInstances

def vm():
	config = open("config/cli.env",'r')
    env = readlines(config)
    config.close()
    for var in env:
        keyVal = split(var,"=")
        os.environ[keyVal[0]] = keyVal[1]
    instance = launchInstances(os.environ[AWS_KEY],os.environ[INSTANCE_TYPE],os.environ[SECURITY_GROUP])
    