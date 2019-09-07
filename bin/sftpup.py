#!/usr/bin/env python3
# coding: utf-8

import boto3, argparse, subprocess
from os import environ, path
from sys import exit
from time import sleep

# from https://aws.amazon.com/fr/about-aws/global-infrastructure/regional-product-services/
POSSIBLES_REGIONS = [
    'us-east-1',
    'us-east-2', 
    'us-west-1', 
    'us-west-2', 
    'ap-south-1', 
    'ap-northeast-1',
    'ap-northeast-2',
    'ap-southeast-1',
    'ap-southeast-2',
    'ca-central-1',
    'eu-central-1',
    'eu-west-1',
    'eu-west-2',
    'eu-west-3',
    'eu-north-1',
    'sa-east-1'
]

def create_ssh_key():
    '''create a new ssh keypair'''
    key_path = environ.get('HOME')+"/.ssh/sftpud"
    subprocess.call(['ssh-keygen', '-t', 'rsa', '-N', '', '-f', key_path])

    with open(key_path+".pub", 'r') as f:
        pubkey = f.read()

    return pubkey

parser = argparse.ArgumentParser(description="sftpud - Pop your own sftp server with AWS")
parser.add_argument('-r', '--region', type=str, help='the region in which you want your SFTP server', required=True)
parser.add_argument('-u', '--user', type=str, help='the user to connect to your SFTP server')
parser.add_argument('-a', '--arn', type=str, help='the arn to awstransfersftp IAM role', required=True)
parser.add_argument('-k', '--key', type=str, help='if you want to use a personnal key to connect to your sftp')
args = vars(parser.parse_args())

region = args['region']
user = environ.get('USERNAME')
iam_role_arn = args['arn']
ssh_key = None
key_path = "~/.ssh/sftpud"

if region not in POSSIBLES_REGIONS:
    print("AWS Transfer for SFTP cannot run in the region", region, ": please recheck.")
    exit(1)

if args['user']:
    user = args['user']

if args['key']:
    key_path = args['key']
    public_key = key_path+".pub"
    if path.exists(public_key):
        with open(public_key, 'r') as f:
            ssh_key = f.read()


sftp = boto3.client('transfer', region_name=region)

if ssh_key is None :
    ssh_key = create_ssh_key()

server = sftp.create_server()
server_data = sftp.describe_server(ServerId=server['ServerId'])
endpoint = server['ServerId']+".server.transfer."+region+".amazonaws.com"

sftp.create_user(
    ServerId=server['ServerId'],
    SshPublicKeyBody=ssh_key,
    Role=iam_role_arn, 
    UserName=user
)

print("Job's done. Server's being created by AWS now.")
print("[...]")
sleep(300)
print("OK, connect with : sftp -i", key_path, user+"@"+endpoint, "\n")
print("You're welcome.")

exit(0)