import sqlite3

class Pokemon:
	def __init__(
			self, id: int, name: str, type1: str, type2: str, gen: int, abilities: str, hp: int, speed: int,
			attack: int, defense: int, classification: str, height: int, weight: int, is_leg: bool):
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

	@classmethod
	def from_db(cls, index: int):
		con = sqlite3.connect("poke.db")
		cursor = con.cursor()
		sql = f"Select * from pokemon where pokedex_number = {index}"
		cursor.execute(sql)
		row = cursor.fetchone()
		con.close()
		return cls(*row)

	def to_db(self):
		connection = sqlite3.connect("poke.db")  # Muss vorher angelegt werden.
		cursor = connection.cursor()
		sql = (
			f'INSERT INTO pokemon(pokedex_number, name, type1, type2, generation, abilities, hp, speed, attack, defense, classfication, height_m, weight_kg, is_legendary) VALUES '
			f'("{self.id}", "{self.name}", "{self.type1}", "{self.type2}", "{self.generation}", "{self.abilities}", "{self.hp}", "{self.speed}", "{self.attack}", "{self.defense}", "{self.classification}", "{self.height}", "{self.weight}", "{self.is_legendary}")')
		cursor.execute(sql)
		connection.commit()
		connection.close()

	def __str__(self) -> str:
		return f"{self.id}: {self.name}"

	def __repr__(self) -> str:
		return f"{self.id}: {self.name}"

def filter_pokemon(key: str, value: str|int, order="asc"):
	con = sqlite3.connect("poke.db")
	cursor = con.cursor()
	sql = f'Select * from pokemon where "{key}" = "{value}" order by "pokedex_number" {order}'
	cursor.execute(sql)
	row = cursor.fetchall()
	con.close()
	return [Pokemon(*entry) for entry in row]

print(filter_pokemon("is_legendary", "1", order="desc"))
# Test case
# l = Pokemon(1000, "IDK", "a", "a", 1, ['a'], 1, 1, 1, 1, "a", 1, 1, 1)
# l.to_db()

