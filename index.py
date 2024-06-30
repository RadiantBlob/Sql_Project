from flask import Flask, render_template, request, redirect

from backend import Pokemon, return_all, return_filter
from user import User

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    ftr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    pokemon_list = return_all(f=ftr)
    if request.method == 'POST':
        number = request.form.get('Number')
        id = request.form.get('ID')
        name = request.form.get('Name')
        type1 = request.form.get('type1')
        type2 = request.form.get('type2')
        generation = request.form.get('Generation')
        abilities = request.form.get('Abilities')
        hp = request.form.get('hp')
        speed = request.form.get('speed')
        attack = request.form.get('attack')
        defense = request.form.get('defense')
        classification = request.form.get('classification')
        height = request.form.get('height')
        weight = request.form.get('weight')
        legendary = request.form.get('legendary')

        checkbox(id, 0, ftr)
        checkbox(name, 1, ftr)
        checkbox(type1, 2, ftr)
        checkbox(type2, 3, ftr)
        checkbox(generation, 4, ftr)
        checkbox(abilities, 5, ftr)
        checkbox(hp, 6, ftr)
        checkbox(speed, 7, ftr)
        checkbox(attack, 8, ftr)
        checkbox(defense, 9, ftr)
        checkbox(classification, 10, ftr)
        checkbox(height, 11, ftr)
        checkbox(weight, 12, ftr)
        checkbox(legendary, 13, ftr)

        if number != '':
            pokemon_list1 = return_filter('pokedex_number', f'{number}', f=ftr)
            return render_template("home.html",
                                   lable=pokemon_list1[0].get_keys(),
                                   entries=[pokemon.get_values() for pokemon in pokemon_list1])
        else:
            pokemon_list2 = return_all(f=ftr)
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


def checkbox(attribute, number, ftr):
    if attribute:
        ftr[number] = '1'
    else:
        ftr[number] = '0'


if __name__ == '__main__':
    app.run()
