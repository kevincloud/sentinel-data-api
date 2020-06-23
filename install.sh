#!/bin/bash

INSTALL_PATH=$(dirname $0)
INSTALL_PATH=$( cd $INSTALL_PATH && pwd )

pip3 install -r /root/sentinel-data-api/requirements.txt

mkdir -p /opt/data-api
cp /root/sentinel-data-api/api.py /opt/data-api/
cp -R /root/sentinel-data-api/classes /opt/data-api/
mkdir -p /opt/web-app
cp /root/sentinel-data-api/app.py /opt/web-app/
cp -R /root/sentinel-data-api/templates /opt/web-app/
cp -R /root/sentinel-data-api/static /opt/web-app/

sudo bash -c "cat >>/opt/web-app/app.ini" <<EOT
[App]
Identifier=$1
AccountKey=$2
EOT

sudo bash -c "cat >>/opt/data-api/app.ini" <<EOT
[App]
Identifier=$1
AccountKey=$2
EOT

# Add API service
echo "Installing systemd service for API..."
sudo bash -c "cat >/etc/systemd/system/sentineldata.service" <<EOT
[Unit]
Description=Sentinel Data Service
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/opt/data-api
ExecStart=/usr/bin/python3 /opt/data-api/api.py
Restart=on-failure # or always, on-abort, etc
[Install]
WantedBy=multi-user.target
EOT

sudo systemctl enable sentineldata
sudo systemctl start sentineldata

# Add Front-end service
echo "Installing systemd service for Web..."
sudo bash -c "cat >/etc/systemd/system/sentinelweb.service" <<EOT
[Unit]
Description=Sentinel Web Service
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/opt/web-app
ExecStart=/usr/bin/python3 /opt/web-app/app.py
Restart=on-failure # or always, on-abort, etc
[Install]
WantedBy=multi-user.target
EOT

sudo systemctl enable sentinelweb
sudo systemctl start sentinelweb

curl http://localhost:8080/reset
