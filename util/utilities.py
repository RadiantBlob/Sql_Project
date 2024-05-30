import sqlite3


def read_one(file: str, sql: str) -> ():
    con = sqlite3.connect(file)
    cursor = con.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    con.close()
    return row


def read_all(file: str, sql: str) -> [()]:
    con = sqlite3.connect(file)
    cursor = con.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    con.close()
    return rows


def write_all(file: str, sql: str):
    connection = sqlite3.connect(file)  # Muss vorher angelegt werden.
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    pass
# print(read_one("../poke.db", "Select * from User"))
