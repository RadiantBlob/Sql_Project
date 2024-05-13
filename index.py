from flask import Flask, render_template, url_for
from backend import Pokemon, return_all

app = Flask(__name__)

@app.route("/")
def index():
	pokemon_list = return_all(f="111111111111110")
	return render_template("home.html",
	                       lable=pokemon_list[0].get_keys(),
	                       entries=[pokemon.get_values() for pokemon in pokemon_list])

@app.route("/pokemon/<int:id>")
def show_pokemon(id: int):
	return render_template("poke-page.html", p=Pokemon.from_db(id))


if __name__ == '__main__':
	app.run()
