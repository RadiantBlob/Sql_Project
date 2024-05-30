import sqlite3
from backend import Pokemon
from util.utilities import read_one, read_all, write_all


# SELECT username, name from User_hat_Pokemon JOIN User on user = username
# JOIN Pokemon on pokemon = pokedex_number

class User:
    def __init__(self, username: str, password: str):
        self.inventory: [[Pokemon, int]] = []
        self.team: list[[Pokemon, int]] = []
        self.username: str = username
        self._password: str = password
        self.p_list: [Pokemon] = []
        self.load_pokemon()

    @classmethod
    def from_db(cls, un: str):
        row = read_one("poke.db", f"SELECT * FROM User WHERE username = '{un}'")
        if row is None:
            return
        return cls(*row)

    @classmethod
    def to_db(cls, un: str, pw: str):
        sql = f"INSERT INTO User(username, password) VALUES ('{un}', '{pw}') "
        write_all("poke.db", sql)

    def load_pokemon(self):
        self.inventory = []
        self.team = []
        sql = f"SELECT pokemon, level, inteam FROM User_hat_Pokemon WHERE user='{self.username}'"
        id_list = read_all("poke.db", sql)
        for id in id_list:
            if bool(id[2]):
                self.team.append([Pokemon.from_db(id[0]), id[1]])
            else:
                self.inventory.append([Pokemon.from_db(id[0]), id[1]])

    # for p in self.inventory:
    # 	p.set_filter("010000000000000")

    def write_pokemon(self, id: int, level: int = 1):
        self.inventory.append([Pokemon.from_db(id), level])
        sql = f"INSERT INTO User_hat_Pokemon (user, pokemon, level) VALUES ('{self.username}', '{id}', '{level}')"
        write_all("poke.db", sql)

    def update_database(self):
        for pokemon, level in self.inventory:
            sql = (f"INSERT INTO User_hat_Pokemon (user, pokemon, level, inteam) VALUES ('{self.username}', '{id}',"
                   f"'{level}', '0')")
            write_all("poke.db", sql)

        for pokemon, level in self.team:
            sql = (f"INSERT INTO User_hat_Pokemon (user, pokemon, level, inteam) VALUES ('{self.username}', '{id}',"
                   f"'{level}', '1')")
            write_all("poke.db", sql)

    def delete_pokemon(self, id: int, level: int):
        sql = (f"SELECT id FROM User_hat_Pokemon WHERE user = '{self.username}' AND pokemon = '{id}'"
               f" and level = '{level}'")
        p = read_one("poke.db", sql)
        if p is None:
            return

        sql = f"DELETE FROM User_hat_Pokemon WHERE id = '{p[0]}'"
        con = sqlite3.connect("poke.db")
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        con.close()
        self.inventory = []
        self.load_pokemon()

    def move_to_team(self, pokemon, level):
        sql = (f"UPDATE User_hat_Pokemon SET inteam = 1 WHERE id = (SELECT id FROM User_hat_Pokemon WHERE pokemon ="
               f"'{pokemon}' AND level = '{level}' limit 1)")
        write_all("poke.db", sql)
        self.load_pokemon()

    def move_to_inventory(self, pokemon, level):
        sql = (f"UPDATE User_hat_Pokemon SET inteam = 0 WHERE id = (SELECT id FROM User_hat_Pokemon WHERE pokemon = "
               f"'{pokemon}' AND level = '{level}' LIMIT 1)")
        write_all("poke.db", sql)
        self.load_pokemon()

    def __str__(self):
        return f"{self.username}"


if __name__ == '__main__':
    admin = User.from_db("admin")
    User.to_db('volmiur', 'test')
    # print(admin.inventory)
    # admin.write_pokemon(135)
    # print(admin.inventory)
    # admin.delete_pokemon(135, 1)
    # admin.move_to_team(4, 2)
    print(admin.inventory)
    print(admin.team)
