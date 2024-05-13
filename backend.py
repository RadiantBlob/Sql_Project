import sqlite3
from typing import Any

# SELECT username, name from User_hat_Pokemon JOIN User on user = username
# JOIN Pokemon on pokemon = pokedex_number

class Pokemon:
	def __init__(
			self, id: int, name: str, type1: str, type2: str, gen: int, abilities: str, hp: int, speed: int,
			attack: int, defense: int, classification: str, height: int, weight: int, is_leg: bool|int, filter_p=None):
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
			self.filter_p =  [True for a in range(len(vars(self)))]
			self.filter_p.append(False)
		else:
			self.filter_p = filter_p


	@classmethod
	def from_db(cls, index: int):
		con = sqlite3.connect("poke.db")
		cursor = con.cursor()
		sql = f"Select * from Pokemon where pokedex_number = {index}"
		cursor.execute(sql)
		row = cursor.fetchone()
		con.close()
		return cls(*row)

	def to_db(self):
		connection = sqlite3.connect("poke.db")  # Muss vorher angelegt werden.
		cursor = connection.cursor()
		sql = (
			f'INSERT INTO Pokemon(pokedex_number, name, type1, type2, generation, abilities, hp, speed, attack, defense, classfication, height_m, weight_kg, is_legendary) VALUES '
			f'("{self.id}", "{self.name}", "{self.type1}", "{self.type2}", "{self.generation}", "{self.abilities}", "{self.hp}", "{self.speed}", "{self.attack}", "{self.defense}", "{self.classification}", "{self.height}", "{self.weight}", "{self.is_legendary}")')
		cursor.execute(sql)
		connection.commit()
		connection.close()

	def set_filter(self, fltr: str):
		if not len(fltr) == 15:
			raise IndexError("fltr has to be 15 chars long")
		self.filter_p = [(False, True)[int(a)] for a in list(fltr)]

	def get_filtered(self) -> [int|str|bool|list]:
		return [str(a) for index, a in enumerate(vars(self).values()) if self.filter_p[index]]

	def __str__(self) -> str:
		return " ".join([str(a) for index, a in enumerate(vars(self).values()) if self.filter_p[index]])

	def __repr__(self) -> str:
		return " ".join([a for index, a in enumerate(vars(self).values()) if self.filter_p[index]])

def return_sql(sql:str) -> [Pokemon]:
	con = sqlite3.connect("poke.db")
	cursor = con.cursor()
	cursor.execute(sql)
	row = cursor.fetchall()
	con.close()
	return [Pokemon(*entry) for entry in row]

def return_filter(key: str, value: str | int, order="asc") -> [Pokemon]:
	return return_sql(f'Select * from Pokemon where "{key}" = "{value}" order by "pokedex_number" {order}')

def return_all() -> [Pokemon]:
	return return_sql(f'Select * from Pokemon')


if __name__ == '__main__':
	# print(return_filter("name", "Bulbasaur"))
	# Test case
	l = Pokemon(1000, "ID", "TR", "TR", 1234, [''], 1234, 1234, 1234, 1234, "TR", 1234, 1234, 1)
	l = Pokemon.from_db(1)
	l.set_filter("111100000000000")
	# print(l.filter_p)
	# print(list(vars(l).values()))
	print(str(l))
	print(l.get_filtered())
	# l.to_db()
