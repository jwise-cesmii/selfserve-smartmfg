from graphql_client import GraphQLClient

client = GraphQLClient('https://gql.annualmeeting.cesmii.thinkiq.net/graphql')

def sendFridgeDoorSample(value, utcdatetime):
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
