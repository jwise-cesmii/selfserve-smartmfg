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

#make another open-ended query
client = GraphQLClient('https://codepoet-sw.herokuapp.com')
result = client.query('''
query {
	allPeople {
		people {
			id,
			name
		}
	}
}
''')
print("Star Wars Characters:")
#print(str(result))

#try a specific query
client = GraphQLClient('https://codepoet-sw.herokuapp.com')
result = client.query('''
query {
	film(id: "ZmlsbXM6MQ==") {
		title,
		releaseDate
	}
}
''')
print("Star Wars Film:")
print(str(result))

#make a specific query passing in an argument
def queryFilmById(filmID):
	#$id is the query's variable
	#ID! is the schema's type
	#filmID is the function's variable, its passed into the query paired with schemas field name
	client = GraphQLClient('https://codepoet-sw.herokuapp.com')
	result = client.query('''
	query FilmById($id:ID!) {
		film(id: $id) {
			title,
			releaseDate
		}
	}
	''', {'id': filmID})
	print("Star Wars Film by ID:")
	print(str(result))
queryFilmById("ZmlsbXM6MQ==")

#try a mutate
client = GraphQLClient('https://codepoet-sw.herokuapp.com')
result = client.query('''
mutation createFilm(
	id: "test123===",
	title: "Jon Strikes Back"
	) {
		id
		title
	}
}
''')
print("Mutation Result:")
print(str(result))