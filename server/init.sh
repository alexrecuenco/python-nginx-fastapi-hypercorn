#!/bin/ash
set -ex

addgroup www-data || echo "Group www-data already exists"
adduser nginx || echo "User nginx already exists"


for i in `seq 0 9`; do
    mkdir -p "/www/uploads/$i"
done

chmod 777 -Rf /www/uploads
