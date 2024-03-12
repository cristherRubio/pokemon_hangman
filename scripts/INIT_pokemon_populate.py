import pandas as pd
from app import create_app, db
from models import Pokemon

#TODO: Read pokemon_data and insert to Pokemon table
df = pd.read_csv('static/pokemon_data.csv')
print(len(df))
df = df[~df.sprite_url.isna()]
df = df[['name', 'type', 'end_url', 'sprite_url']]
print(len(df))
print(df)

#col_names = ('name', 'type', 'end_url', 'sprite_url')
# ChatGPT -- Insert dataframe to DB
app = create_app()
with app.app_context():
    for row in df.itertuples():
        pokemon = Pokemon(name=row[1], type=row[2], end_url=row[3], sprite_url=row[4])
        db.session.add(pokemon)
    db.session.commit()