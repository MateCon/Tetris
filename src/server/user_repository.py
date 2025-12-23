from server_model.database import UserRepository
from server_model.user import User


class PostgresUserRepository(UserRepository):
    def __init__(self, aDatabase):
        self.database = aDatabase

    def insert(self, aUser):
        values = (aUser.name(), aUser.hashedPassword())

        def query(cursor):
            cursor.execute("INSERT INTO tetris_user (name, password) VALUES (%s, %s)", values)

        self.database.execute(query)

    def selectAll(self):
        def query(cursor):
            cursor.execute("SELECT * FROM tetris_user")
            return cursor.fetchall()

        rows = self.database.execute(query)

        users = []
        for row in rows:
            users.append(User(row[0], row[1]))

        return users
