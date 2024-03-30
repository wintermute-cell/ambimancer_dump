#!/bin/env sh

export GUN_PORT=4000
export GUN_IP=127.0.0.1
#192.168.178.34
gunicorn app:app -b $GUN_IP:$GUN_PORT

