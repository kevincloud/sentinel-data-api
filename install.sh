#!/bin/bash

INSTALL_PATH=$(dirname $0)
INSTALL_PATH=$( cd $INSTALL_PATH && pwd )

pip3 install -r $INSTALL_PATH/requirements.txt

mkdir -p /opt/data-api
cp $INSTALL_PATH/api.py /opt/data-api/
cp -R $INSTALL_PATH/classes /opt/data-api/
mkdir -p /opt/web-app
cp $INSTALL_PATH/app.py /opt/web-app/
cp -R $INSTALL_PATH/templates /opt/web-app/
cp -R $INSTALL_PATH/static /opt/web-app/

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

curl -s http://localhost:8080/reset
