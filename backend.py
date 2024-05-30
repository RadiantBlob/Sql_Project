import sqlite3
from util.utilities import read_one, read_all, write_all
from typing import Any


# SELECT username, name from User_hat_Pokemon JOIN User on user = username
# JOIN Pokemon on pokemon = pokedex_number

class Pokemon:
    def __init__(
            self, id: int, name: str, type1: str, type2: str, gen: int, abilities: str, hp: int, speed: int,
            attack: int, defense: int, classification: str, height: int, weight: int, is_leg: bool | int,
            filter_p=None):
        self.id: int = id
        self.name: str = name
        self.type1: str = type1
        self.type2: str = type2
        self.generation: int = gen
        self.abilities: str = abilities
        self.hp: int = hp
        self.speed: int = speed
        self.attack: int = attack
        self.defense: int = defense
        self.classification: str = classification
        self.height: int = height
        self.weight: int = weight
        self.is_legendary: bool = is_leg
        if filter_p is None:
            self.filter_p = [True for a in range(len(vars(self)))]
            self.filter_p.append(False)
        else:
            self.filter_p = filter_p

    @classmethod
    def from_db(cls, index: int):
        row = read_one("poke.db", f"SELECT * FROM Pokemon WHERE pokedex_number = {index}")
        return cls(*row)

    def to_db(self):
        sql = (
            f'INSERT INTO Pokemon(pokedex_number, name, type1, type2, generation, abilities, hp, speed, attack, '
            f'defense, classfication, height_m, weight_kg, is_legendary) VALUES'
            f'("{self.id}", "{self.name}", "{self.type1}", "{self.type2}", "{self.generation}", "{self.abilities}", '
            f'"{self.hp}", "{self.speed}", "{self.attack}", "{self.defense}", "{self.classification}", '
            f'"{self.height}", "{self.weight}", "{self.is_legendary}")')
        write_all("poke.db", sql)

    def set_filter(self, fltr: str):
        if not len(fltr) == 15:
            raise IndexError("fltr has to be 15 chars long")
        self.filter_p = [(False, True)[int(a)] for a in list(fltr)]

    def get_values(self) -> [int | str | bool | list]:
        return [str(a) for index, a in enumerate(vars(self).values()) if self.filter_p[index]]

    def get_keys(self) -> [str]:
        return [str(a) for index, a in enumerate(vars(self).keys()) if self.filter_p[index]]

    def __str__(self) -> str:
        return " ".join([str(a) for index, a in enumerate(vars(self).values()) if self.filter_p[index]])

    def __repr__(self) -> str:
        return " ".join([str(a) for index, a in enumerate(vars(self).values()) if self.filter_p[index]])


def return_sql(sql: str, f="111111111111110") -> [Pokemon]:
    row = read_all("poke.db", sql)

    pokemon_list = [Pokemon(*entry, filter_p=[True for a in range(14)]) for entry in row]
    for p in pokemon_list:
        p.set_filter(f)
    return pokemon_list


def return_filter(key: str, value: str | int, order="asc", f="111111111111110") -> [Pokemon]:
    return return_sql(f'SELECT * FROM Pokemon WHERE "{key}" = "{value}" ORDER BY "pokedex_number" {order}', f)


def return_all(f="111111111111110") -> [Pokemon]:
    return return_sql(f'SELECT * FROM Pokemon', f)


if __name__ == '__main__':
    pass
# Test case
# l = Pokemon(1000, "ID", "TR", "TR", 1234, [''], 1234, 1234, 1234, 1234, "TR", 1234, 1234, 1)
# l = Pokemon.from_db(1)
# l.set_filter("111100000000000")
# print(return_filter('pokedex_number', 10))
# print(l.filter_p)
# print(list(vars(l).values()))
# print(str(l))
# print(l.get_keys())
# print(l.get_values())
# l.to_db()
