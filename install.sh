#!/bin/bash

sudo pip install -r requirements.txt

sudo cp bin/sftpdown.py /usr/local/bin/sftpdown
sudo cp bin/sftpup.py /usr/local/bin/sftpup

echo "yay!"