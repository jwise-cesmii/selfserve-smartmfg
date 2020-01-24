#this library didn't work
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

client = Client(
	retries=1,
	transport=RequestsHTTPTransport(
		url='http://codepoet-sw.herokuapp.com/', 
		headers={
			'Content-Type':'application/json', 
			'Accepts':'application/json'
		}
	)
)
query = gql('''
{
	allFilms {
		films {id, title}
	}
}
''')

client.execute(query)

