#!/usr/bin/env python3
# coding: utf-8

import boto3
import argparse
from sys import exit
from os import remove

parser = argparse.ArgumentParser(description="sftpdown - shutdown your AWS sftp server")
parser.add_argument('-r', '--region', type=str, help='region of your SFTP server', required=True)
parser.add_argument('-i', '--id', type=str, help='the id of your sftp server', required=True)
args = vars(parser.parse_args())

region = args['region']
sftp_id = args['id']

sftp = boto3.client('transfer', region_name=region)

if __name__ == '__main__':
    try:
        sftp.delete_server(ServerId = sftp_id)
    except:
        print("There was an error. Please check id and region.")
        exit(1)

print("Your server", sftp_id, "in region", region, "was deleted.")