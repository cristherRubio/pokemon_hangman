import csv
import time
import requests
import pandas as pd

# PokéAPI request to get all names
url = "https://pokeapi.co/api/v2/pokemon/?limit=100000&offset=0"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Extracting names from the results
    pokemon_names = [pokemon['name'] for pokemon in data['results']]
else:
    print("Failed to retrieve data:", response.status_code)

pokemon_names = sorted(pokemon_names)

counter = 1
poke_data = []
for pk in pokemon_names:
    if counter % 50 == 0:
        time.sleep(30)
    url = f"https://pokeapi.co/api/v2/pokemon/{pk}"
    response = requests.get(url)
    if response.status_code == 200:
        print(pk)
        data = response.json()
        sprite = data['sprites']['front_default']
        type = data['types'][0]['type']['name']
        poke_data.append({'name': pk.split('-')[0], 'type': type, 'end_url': pk, 'sprite_url': sprite})
    else:
        print(f"Failed to retrieve {pk} data:", response.status_code)

    counter += 1

columns = poke_data[0].keys()
pd.DataFrame(poke_data, columns=columns).to_csv('pokemon_data.csv')