import sqlite3


class DB_Connection:
    def __init__(self):
        self._connection = None

    def __enter__(self):
        self._connection = sqlite3.connect("shortener.db")
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
        if exc_type:
            print(f'dblib Error: {exc_val}')


def set_db():
    db_exec("CREATE TABLE Sites(id, url, title)")


def append_site(id: str, url, title):
    db_exec(f"INSERT INTO Sites VALUES ('{id}', '{url}', '{title}')")


def get_max_site_id():
    max_id = db_exec(f"SELECT MAX(id) from Sites")
    if max_id:
        max_id = max_id[0][0]
    return max_id


def get_site(id):
    if site := db_exec(f"SELECT id, url, title FROM Sites WHERE id = '{id}'"):
        site = site[0]

    return site


def get_usage():
    stats = db_exec(f"SELECT url, count(*) as cant from Sites GROUP BY url ORDER BY count(*) desc LIMIT 100")
    return stats


def db_exec(command, *args) -> list[sqlite3.dbapi2.Cursor]:
    with DB_Connection() as connection:
        cursor = connection.cursor()
        result = cursor.execute(command, *args).fetchall()
        connection.commit()

    return result



