from flask import Flask, render_template

from backend import Pokemon, return_all

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("home.html",
	                       lable=vars(Pokemon.from_db(1)).keys(),
	                       entries=[list(vars(pokemon).values()) for pokemon in
	                                return_all()])


if __name__ == '__main__':
	# print(vars(Pokemon.from_db(1)).keys())

	app.run()
