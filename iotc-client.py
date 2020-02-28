# Based on https://github.com/Azure/iot-central-firmware
# Copyright (c) Microsoft. All rights reserved.
# Extensions and improvements by Jon W, 2020
# Licensed under the MIT license.

import iotc
from iotc import IOTConnectType, IOTLogLevel
import locationlib
import networklib
import gqlthinkiq
import smbus2
import bme280
import psutil
import os.path
import configparser
from gpiozero import LED, CPUTemperature, Button
from binascii import unhexlify
from random import randint
from time import sleep
from datetime import datetime

print ("")
print ("Azure IOT Central Client")
print ("========================")
print ("")
sleep(40)

#load local config
picFile = os.path.join(os.path.expanduser("~"), "picam.jpg")
configFile = os.path.join(os.path.expanduser("~"), "iotc.config") 
config = configparser.ConfigParser()
config.read(configFile)
print ("Loading configuration from " + configFile + " ...")
sampleInterval=int(config.get("Settings", "sampleInterval"))
statusLEDPin=int(config.get("Settings", "statusLEDPin"))
commandLEDPin=int(config.get("Settings", "commandLEDPin"))
doorSensorPin=int(config.get("Settings", "doorSensorPin"))
global currLocation
currLocation=str(config.get("Settings", "defaultLocation"))   #{\"lon\":\"-81.20288\", \"lat\":\"41.58339\" }
ledStatus = LED(statusLEDPin)
global useStatusLight
useStatusLight = True

#GPIO Config
ledCommand = LED(commandLEDPin)
cpu = CPUTemperature()
door = Button(doorSensorPin)
print ("Sample interval: " + str(sampleInterval))
print ("Status LED Pin: " + str(statusLEDPin))
print ("Command LED Pin: " + str(commandLEDPin))
print ("Door Sensor Pin: " + str(doorSensorPin))
print ("")

#BME sensor config
port=int(config.get("Sensors", "BMEPort"))
address=config.get("Sensors", "BMEAddress")
hexaddress = int(address, 16)
print ("Using Sensor values ...")
print ("BMEPort: " + str(port))
print ("BMEAddress: '" + hex(hexaddress) + "'")
print("")
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, hexaddress)

#Azure settings
deviceId = str(config.get("AzureKeys", "deviceId"))
scopeId = str(config.get("AzureKeys", "scopeId"))
deviceKey = str(config.get("AzureKeys", "deviceKey"))
print ("Using Azure values ...")
print ("deviceId: " + deviceId)
print ("scopeId: " + scopeId)
print ("deviceKey: " + deviceKey)
print("")
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
      updateLocation()

def onmessagesent(info):
  print("\t- [onmessagesent] => " + str(info.getPayload()))

def oncommand(info):  # handle commands sent from Azure
  print("- [oncommand] => " + info.getTag() + " => " + str(info.getPayload()))
  if info.getTag() == "toggleLED": 
    ledCommand.toggle()
  if info.getTag() == "updateLocation":
    updateLocation()
  if info.getTag() == "scanNetwork":
    networkCount = networklib.getNetDeviceCount()
    iotc.sendProperty('{"netDeviceCount":"' + networkCount + '"}')

def onsettingsupdated(info):  # handle settings set by Azure
  global useStatusLight
  print("- [onsettingsupdated] => " + info.getTag() + " => " + info.getPayload())
  if info.getTag() == "useStatusLight":
      if 'true' in info.getPayload():
        useStatusLight = True
      else:
        useStatusLight = False

def updateLocation():
    global currLocation
    currLocation = locationlib.getlocationLonLat()
    iotc.sendProperty('{"currCity":"' + locationlib.getlocationCity() + '"}')
    iotc.sendTelemetry('{"currLocation":' + currLocation + '}')

#update loop
def sendTelemetry():
  while iotc.isConnected():
    iotc.doNext() # do the async work needed to be done for MQTT
    if gCanSend == True:
        print("[" + str(datetime.now()) + "] Sending telemetry...")
        if useStatusLight == True:
          ledStatus.on()
        sensordata = bme280.sample(bus, hexaddress, calibration_params)
        doorState = 1
        if door.is_pressed == True:
          doorState = 0
        #send to Azure
        iotc.sendTelemetry("{ \
\"doorOpen\": " + str(doorState) + ", \
\"ambientTemp\": " + str(sensordata.temperature) + ", \
\"cpuTemp\": " + str(cpu.temperature) + ", \
\"cpuLoad\": " + str(psutil.cpu_percent()) + ", \
\"randomNum\": " + str(randint(1, 99)) + ", \
\"humidity\": " + str(sensordata.humidity) + ", \
\"pressure\": " + str(sensordata.pressure) + "}")
        #send to ThinkIQ
        gqlthinkiq.sendFridgeDoorSample(str(doorState))
        gqlthinkiq.sendFridgeHumiditySample(str(sensordata.humidity))
        gqlthinkiq.sendFridgeTemperatureSample(str(sensordata.temperature))
        #global picFile
        #os.system("raspistill -w 640 -h 480 -o " + picFile)
        ledStatus.off()
        sleep(sampleInterval)

iotc.on("Command", oncommand)
iotc.on("ConnectionStatus", onconnect)
iotc.on("MessageSent", onmessagesent)
iotc.on("SettingsUpdated", onsettingsupdated)

while True:
  iotc.connect()
  iotc.sendProperty('{"runNumber":' + str(randint(1,10000)) + '}')
  sendTelemetry()
  sleep(40)
