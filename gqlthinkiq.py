from graphql_client import GraphQLClient
from time import gmtime, strftime

client = GraphQLClient('https://gql.annualmeeting.cesmii.thinkiq.net/graphql')

def makeutcdatetime()
  timestamp = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
  timestamp = timestamp + "-05:00"
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
        tagId: "1847"
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
        tagId: "1847"
      }) {
      string
    }
  }
  ''')
  print("ThinkIQ Mutate:")
  print(str(result))