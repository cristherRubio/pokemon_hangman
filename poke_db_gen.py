import requests

# PokéAPI request to get all names
url = "https://pokeapi.co/api/v2/pokemon/?limit=100000&offset=0"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Extracting names from the results
    pokemon_names = [pokemon['name'].split('-')[0] for pokemon in data['results']]
else:
    print("Failed to retrieve data:", response.status_code)

with open('pokemons.txt', mode='w') as f:
    for pokemon in pokemon_names:
        f.write(pokemon + '\n')