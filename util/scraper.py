import requests
import sqlite3

con = sqlite3.connect("../poke.db")
cursor = con.cursor()
sql = f"Select pokedex_number, name from Pokemon order by pokedex_number asc"
cursor.execute(sql)
row = cursor.fetchall()
con.close()

for id, name in dict(row).items():
    img_data = requests.get(f"https://img.pokemondb.net/artwork/vector/{name.lower().replace(' ', '-')}.png") # Global Link
    # img_data = requests.get(f"https://img.pokemondb.net/artwork/large/{name.lower().replace(' ', '-')}.jpg") # Sugimori Art
    if not img_data.ok:
        print(id, name)
        continue

    with open(f'static/other-sprites/{id}.png', 'wb') as handler:
        handler.write(img_data.content)
