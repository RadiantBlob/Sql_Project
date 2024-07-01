from flask import Flask, render_template, request, redirect, url_for
from backend import Pokemon, return_all, return_filter
from user import User

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    argument_filter = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    filter_arguments = ['ID', 'Name', 'type1', 'type2', 'Generation', 'Abilities', 'hp', 'speed',
                        'attack', 'defense', 'classification', 'height', 'weight', 'legendary']

    pokemon_list = return_all(f=argument_filter)
    dict_arg_val = dict(zip(filter_arguments, argument_filter)) 

    if request.method == 'POST':
        number = request.form.get('Number')

        filter_arg_values = {arg: request.form.get(arg) for arg in filter_arguments}
        filter_values = list(filter_arg_values.values())
        argument_filter = [0 if val is None else 1 for val in filter_values]
        argument_filter.append(0)

        dict_arg_val = dict(zip(filter_arguments, argument_filter)) 

        if number != '':
            pokemon_list = return_filter('pokedex_number', f'{number}', f=argument_filter)
        else:
            pokemon_list = return_all(f=argument_filter)

    return render_template("home.html",
                           lable=pokemon_list[0].get_keys(),
                           entries=[pokemon.get_values() for pokemon in pokemon_list],
                           pokemon_list=pokemon_list,
                           checkboxes=dict_arg_val)


@app.route("/pokemon/<int:id>")
def show_pokemon(id: int):
    return render_template("poke-page.html", p=Pokemon.from_db(id))


@app.route("/add/<int:id>")
def add(id: int):
    return show_pokemon(id)


@app.route("/u/<string:username>", methods=['GET', 'POST'])
def user(username: str, login=False):
    u = User.from_db(username)
    if request.method == 'GET':
        login = request.args.get('login')
    if request.method == 'POST' and request.form.get('name') is not None:
        pokemon_name = request.form.get('name')
        pokemon_level = request.form.get('level')
        User.move_to_inventory(pokemon_name, pokemon_level, u)
        return render_template("user.html", user=u, login=True)
    elif request.method == 'POST' and request.form.get('name1') is not None:
        pokemon_name = request.form.get('name1')
        pokemon_level = request.form.get('level1')
        User.move_to_team(pokemon_name, pokemon_level, u)
        return render_template("user.html", user=u, login=True)
    elif request.method == 'POST':
        pokemon_id = request.form.get('pokemon_id')
        pokemon_level = request.form.get('pokemon_level')
        User.add_pokemon(pokemon_id, pokemon_level, u)
        return render_template("user.html", user=u, login=True)
    if u is None:
        return "Not a valid username"
    if login:
        return render_template("user.html", user=u, login=True)
    return render_template("user.html", user=u, login=False)


@app.route("/u/add", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        u = User.from_db(username)
        if u is None:
            User.to_db(username, password)
            return redirect(url_for('user', username=username, login=True))

        else:
            return "Username is already used"
    return render_template("add_user.html")


@app.route("/u/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        u = User.from_db(username)
        p = User.password(password)
        if u is None:
            return "Please create an user"
        elif p is None:
            return 'Your password is wrong'
        elif str(p) != str(u):
            return 'Your password is wrong'
        else:
            return redirect(url_for('user', username=username, login=True))
    return render_template("login_user.html")


if __name__ == '__main__':
    app.run()
