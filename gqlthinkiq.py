from graphql_client import GraphQLClient
from time import gmtime, strftime
import os.path
import configparser

configFile = os.path.join(os.path.expanduser("~"), "iotc.config")
config = configparser.ConfigParser()
config.read(configFile)
endpointURL = str(config.get("GraphQL", "endpointURL"))
client = GraphQLClient(endpointURL)

def makeutcdatetime():
  timestamp = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
  print ("time is " + timestamp)
  return timestamp

def sendFridgeDoorSample(value):
  utcdatetime = makeutcdatetime()
  result = client.query('''
  mutation UpdateFridgeData {
    replaceTimeSeriesRange(
      input: {
        entries: [
          {value: "''' + value + '''", timestamp: "''' + utcdatetime + '''", status: "0"}
        ],
        tagId: "1847"
      }) {
      string
    }
  }
  ''')
  print("ThinkIQ Mutate:")
  print(str(result))

def sendFridgeTemperatureSample(value):
  utcdatetime = makeutcdatetime()
  result = client.query('''
  mutation UpdateFridgeData {
    replaceTimeSeriesRange(
      input: {
        entries: [
          {value: "''' + value + '''", timestamp: "''' + utcdatetime + '''", status: "0"}
        ],
        tagId: "1848"
      }) {
      string
    }
  }
  ''')
  print("ThinkIQ Mutate:")
  print(str(result))

def sendFridgeHumiditySample(value):
  utcdatetime = makeutcdatetime()
  result = client.query('''
  mutation UpdateFridgeData {
    replaceTimeSeriesRange(
      input: {
        entries: [
          {value: "''' + value + '''", timestamp: "''' + utcdatetime + '''", status: "0"}
        ],
        tagId: "1832"
      }) {
      string
    }
  }
  ''')
  print("ThinkIQ Mutate:")
  print(str(result))
