# sftpud - pop up your own sftp server via AWS !

## What
The idea came to me when I discovered [this script](https://github.com/ttlequals0/autovpn), which allows you to spin up a VPN into AWS Cloud in one script. 

With sftpud, you can pop up your own sftp server in the region of the world of your choice, in **one single command**. You can also specify if you want a key and a user to connect it.

## How
This repository contains two scripts : sftpup.py and sftpdown.py. These scripts are using [AWS Transfer for SFTP](https://aws.amazon.com/sftp/).

It needs mainly the `boto3` python module, which you can install with:

~~~bash
$ pip install -r requirements.txt
~~~

You're also gonna need :
* the ARN of an IAM role which has AmazonS3FullAccess right
* your AWS credentials up to date in `~/.aws/credentials`.

You can create those two from [the AWS management console](https://console.aws.amazon.com).

For the IAM role, go to [IAM](https://console.aws.amazon.com/iam/) > Roles > Create role > choose Transfer > Give AmazonS3FullAccess right > No tag > Give it a name > Create a role.

Let's see how theses scripts work.

### sftpup

By default, the user is your current connected user, and the key is created in `.ssh/sftpud.pub`. 

So here's an example:

~~~bash
$ sftpup.py -r eu-west-1 -u kharec -a "arn:aws:iam::183593864628:role/awstransfersftp"
~~~

Wait about 5m to get the server online and... Here you go !

If you wanna see the others options, you can do :

~~~bash
$ sftpup.py -h
~~~

### sftpdown
To delete the previously created sftp server, you just have to specify the region and the id.

~~~bash
$ sftpdown.py -r eu-west-1 -i s-7e38802e91a74c369
Your server s-7e38802e91a74c369 in region eu-west-1 was deleted.
~~~

This script can also delete an AWS SFTP server which wasn't created by it.

## Beware
AWS Transfer for SFTP can cost a lot. Find the pricing [here](https://aws.amazon.com/sftp/pricing/).

## Licence & Copyright
This software is copyright (c) 2019 by Sandro CAZZANIGA.

This is free software, you can use/redistribute it and/or modify it under the GNU GPLv3 terms.