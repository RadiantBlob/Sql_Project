import sqlite3
from backend import Pokemon
from util.utilities import read_one, read_all, write_all

# SELECT username, name from User_hat_Pokemon JOIN User on user = username
# JOIN Pokemon on pokemon = pokedex_number

class User:
	def __init__(self, username: str, password: str):
		self.inventory: [Pokemon] = []
		self.username: str = username
		self._password: str = password
		self.p_list: [Pokemon] = []

	@classmethod
	def from_db(cls, un: str):
		row = read_one("poke.db", f"Select * from User where username = '{un}'")
		if row is None:
			return
		return cls(*row)


	def to_db(self):
		sql = f"Insert into User(username, password) values ({self.username, self._password}) "
		write_all("poke.db", sql)


	def load_pokemon(self):
		sql = f"Select pokemon, level from User_hat_Pokemon where user='{self.username}'"
		id_list = read_all("poke.db", sql)
		for id in id_list:
			self.inventory.append((Pokemon.from_db(id[0]), id[1]))
		# for p in self.inventory:
		# 	p.set_filter("010000000000000")

	def __str__(self):
		return f"{self.username}"

if __name__ == '__main__':
	admin = User.from_db("admin")
	admin.load_pokemon()
	print(admin.inventory)