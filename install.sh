#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Install necessary Debian package dependencies
apt-get -y install python pipenv alien libaio1

# Download and install Oracle Instant Client 
instant_client_fn="oracle-instantclient-basic-linuxx64.rpm"

wget "https://download.oracle.com/otn_software/linux/instantclient/$instant_client_fn"

alien -i "$instant_client_fn"

rm "$instant_client_fn"
