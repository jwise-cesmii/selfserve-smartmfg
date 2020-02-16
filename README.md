setup raspberry pi: expand fs, change keyboard layout, join network, apt-get update, etc...

enable I2C and SPI interfaces in raspi-config

sudo apt install python3-pip

sudo apt install nmap

sudo pip3 install nmap

sudo pip3 install python-nmap

sudo pip3 install psutil

sudo apt install python3-gpiozero

sudo pip3 install gpiozero

sudo pip3 install graphql_client

sudo pip3 install iotc

sudo apt-get install i2c-tools

Install BME2380 Sensor, check with i2cdetect -y 1

sudo pip3 install RPi.bme280

cp sample-iotc.config ~/iotc.config

edit ~/iotc.config to add Azure keys from IOTCentral Device config, change BME port or address as needed

One of the tests depends on https://github.com/graphql/swapi-graphql which I deployed to https://codepoet-sw.herokuapp.com/
