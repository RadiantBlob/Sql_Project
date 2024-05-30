from flask import Flask, render_template, request, redirect

from backend import Pokemon, return_all, return_filter
from user import User

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    pokemon_list = return_all(f="111111111111110")
    if request.method == 'POST':
        number = request.form.get('Number')
        fltr = request.form.get('Filter')
        if fltr == '':
            fltr = "111111111111110"
        if number != '':
            pokemon_list1 = return_filter('pokedex_number', f'{number}', f='{filter}'.format(filter=fltr))
            return render_template("home.html",
                                   lable=pokemon_list1[0].get_keys(),
                                   entries=[pokemon.get_values() for pokemon in pokemon_list1])
        else:
            pokemon_list2 = return_all(f='{filter}'.format(filter=fltr))
            return render_template("home.html",
                                   lable=pokemon_list2[0].get_keys(),
                                   entries=[pokemon.get_values() for pokemon in pokemon_list2])

    return render_template("home.html",
                           lable=pokemon_list[0].get_keys(),
                           entries=[pokemon.get_values() for pokemon in pokemon_list])


@app.route("/pokemon/<int:id>")
def show_pokemon(id: int):
    return render_template("poke-page.html", p=Pokemon.from_db(id))


@app.route("/add/<int:id>")
def add(id: int):
    return show_pokemon(id)


@app.route("/u/<string:username>")
def user(username: str):
    u = User.from_db(username)
    if u is None:
        return "Not a valid username"
    return render_template("user.html", user=u)


@app.route("/u/add", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        u = User.from_db(username)
        if u is None:
            User.to_db(username, password)
            return redirect("/u/{username}".format(username=username))
        else:
            return "Username is already used"
    return render_template("add_user.html")


if __name__ == '__main__':
    app.run()
