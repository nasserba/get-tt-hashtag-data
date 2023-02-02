#! /bin/bash

# pip install -U --upgrade pip
# pip install --user -r requirements.txt
pip install -r requirements.txt
/usr/bin/dumb-init -- /entrypoint "$@"