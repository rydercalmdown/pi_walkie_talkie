#!/bin/bash
# configure_on_boot.sh
# Configures the script to run on boot


sudo sed -i.bak '$ i\cd /home/pi/pi_walkie_talkie && make run-client &' /etc/rc.local

echo "New File: ================"
cat /etc/rc.local

echo "Backup /etc/rc.local: ==============="
cat /etc/rc.local.bak
