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
		row = read_one("poke.db", f"Select * from User where username = '{un}'")
		if row is None:
			return
		return cls(*row)


	def to_db(self):
		sql = f"Insert into User(username, password) values ({self.username, self._password}) "
		write_all("poke.db", sql)


	def load_pokemon(self):
		self.inventory = []
		self.team = []
		sql = f"Select pokemon, level, inteam from User_hat_Pokemon where user='{self.username}'"
		id_list = read_all("poke.db", sql)
		for id in id_list:
			if bool(id[2]):
				self.team.append([Pokemon.from_db(id[0]), id[1]])
			else:
				self.inventory.append([Pokemon.from_db(id[0]), id[1]])


		# for p in self.inventory:
		# 	p.set_filter("010000000000000")

	def write_pokemon(self, id: int, level: int=1):
		self.inventory.append([Pokemon.from_db(id), level])
		sql = f"Insert into User_hat_Pokemon (user, pokemon, level) values ('{self.username}', '{id}', '{level}')"
		write_all("poke.db", sql)

	def update_database(self):
		for pokemon, level in self.inventory:
			sql = f"Insert into User_hat_Pokemon (user, pokemon, level, inteam) values ('{self.username}', '{id}', '{level}', '0')"
			write_all("poke.db", sql)

		for pokemon, level in self.team:
			sql = f"Insert into User_hat_Pokemon (user, pokemon, level, inteam) values ('{self.username}', '{id}', '{level}', '1')"
			write_all("poke.db", sql)

	def delete_pokemon(self, id: int, level: int):
		sql = f"Select id from User_hat_Pokemon where user = '{self.username}' and pokemon = '{id}' and level = '{level}'"
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
		sql = f"update User_hat_Pokemon set inteam = 1 where id = (SELECT id from User_hat_Pokemon where pokemon = '{pokemon}' and level = '{level}' limit 1) "
		write_all("poke.db", sql)
		self.load_pokemon()

	def move_to_inventory(self, pokemon, level):
		sql = f"update User_hat_Pokemon set inteam = 0 where id = (SELECT id from User_hat_Pokemon where pokemon = '{pokemon}' and level = '{level}' limit 1) "
		write_all("poke.db", sql)
		self.load_pokemon()

	def __str__(self):
		return f"{self.username}"

if __name__ == '__main__':
	admin = User.from_db("admin")
	# print(admin.inventory)
	# admin.write_pokemon(135)
	# print(admin.inventory)
	# admin.delete_pokemon(135, 1)
	# admin.move_to_inventory(4, 2)
	print(admin.inventory)
	print(admin.team)
