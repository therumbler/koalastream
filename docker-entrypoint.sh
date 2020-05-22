#!/bin/sh
python3 -V
echo "running nginx..."

/usr/local/nginx/sbin/nginx -c /koalastream/conf/nginx.conf
cd /app
pipenv run uvicorn main:api --host 0.0.0.0 --log-level debug
