# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import iotc
from iotc import IOTConnectType, IOTLogLevel
import smbus2
import bme280
from gpiozero import LED
from binascii import unhexlify
from random import randint
from time import sleep
import os.path
import configparser

#load config
homeDir = os.path.expanduser("~")
configFile = os.path.join(homeDir, "iotc.config")
config = configparser.ConfigParser()
config.read(configFile)
print ("Loading configuration from ...")
print (configFile)
sampleInterval=int(config.get("Settings", "sampleInterval"))
ledPin=int(config.get("Settings", "LEDPin"))
led = LED(ledPin)
print ("Sample interval: " + str(sampleInterval))
print ("LED Pin: " + str(ledPin))

#bme sensor config
port=int(config.get("Sensors", "BMEPort"))
address=config.get("Sensors", "BMEAddress")
hexaddress = int(address, 16)
print ("Using Sensor values ...")
print ("BMEPort: " + str(port))
print ("BMEAddress: '" + hex(hexaddress) + "'")

bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, hexaddress)

#azure config
deviceId = str(config.get("AzureKeys", "deviceId"))
scopeId = str(config.get("AzureKeys", "scopeId"))
deviceKey = str(config.get("AzureKeys", "deviceKey"))
print ("Using Azure values ...")
print ("deviceId: " + deviceId)
print ("scopeId: " + scopeId)
print ("deviceKey: " + deviceKey)

iotc = iotc.Device(scopeId, deviceKey, deviceId, IOTConnectType.IOTC_CONNECT_SYMM_KEY)
iotc.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)

gCanSend = False
gCounter = 0

def onconnect(info):
  global gCanSend
  print("- [onconnect] => status:" + str(info.getStatusCode()))
  if info.getStatusCode() == 0:
     if iotc.isConnected():
       gCanSend = True

def onmessagesent(info):
  print("\t- [onmessagesent] => " + str(info.getPayload()))

def oncommand(info):
  print("- [oncommand] => " + info.getTag() + " => " + str(info.getPayload()))

def onsettingsupdated(info):
  print("- [onsettingsupdated] => " + info.getTag() + " => " + info.getPayload())

iotc.on("ConnectionStatus", onconnect)
iotc.on("MessageSent", onmessagesent)
iotc.on("Command", oncommand)
iotc.on("SettingsUpdated", onsettingsupdated)

iotc.connect()

#update loop
while iotc.isConnected():
  iotc.doNext() # do the async work needed to be done for MQTT
  if gCanSend == True:
      led.on()
      sensordata = bme280.sample(bus, hexaddress, calibration_params)
      print("Sending telemetry..")
      iotc.sendTelemetry("{ \
\"temp\": " + str(sensordata.temperature) + ", \
\"accelerometerX\": " + str(randint(2, 95)) + ", \
\"accelerometerY\": " + str(randint(3, 69)) + ", \
\"accelerometerZ\": " + str(randint(3, 75)) + ", \
\"gyroscopeX\": " + str(randint(3, 32)) + ", \
\"gyroscopeY\": " + str(randint(32, 80)) + ", \
\"gyroscopeZ\": " + str(randint(10, 90)) + ", \
\"humidity\": " + str(sensordata.humidity) + ", \
\"pressure\": " + str(sensordata.pressure) + "}")
      sleep(sampleInterval)
      led.off()
