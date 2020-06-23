#!/bin/bash

cp /root/sentinel-data-api/api.py /opt/data-api/
cp -R /root/sentinel-data-api/classes /opt/data-api/
cp /root/sentinel-data-api/app.py /opt/web-app/
cp -R /root/sentinel-data-api/templates /opt/web-app/
cp -R /root/sentinel-data-api/static /opt/web-app/

service sentineldata restart
service sentinelweb restart
