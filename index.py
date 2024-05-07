from flask import Flask, render_template, url_for
from backend import Pokemon, return_all

app = Flask(__name__)

@app.route("/")
def index():

	return render_template("home.html",
	                       lable=vars(Pokemon.from_db(1)).keys(),
	                       entries=[list(vars(pokemon).values()) for pokemon in
	                                return_all()])

@app.route("/pokemon/<int:id>")
def show_pokemon(id: int):
	return render_template("poke-page.html", p=Pokemon.from_db(id))


if __name__ == '__main__':
	app.run()
