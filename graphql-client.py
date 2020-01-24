from graphql_client import GraphQLClient

#make open-ended query
client = GraphQLClient('https://codepoet-sw.herokuapp.com')
result = client.query('''
query {
	allFilms {
		films {
			id,
			title
		}
	}
}
''')
print("Star Wars Films:")
print(str(result))

#make query for specific object
client = GraphQLClient('https://www.graphqlhub.com/graphql')
result = client.query('''
query ($id:String!) {
	hn2 {
		nodeFromHnId(id: $id, isUserId: true) {
			id
		}
	}
}
''', {'id': 'clayallsopp'})
print("User:")
print(str(result))
