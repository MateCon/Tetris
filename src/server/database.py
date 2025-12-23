import psycopg
from server.user_repository import PostgresUserRepository
from server.session_repository import PostgresSessionRepository
from server_model.database import Database


class PostgresDatabase(Database):
    def __init__(self, aConnectionString):
        self.connectionString = aConnectionString
        self.connection = psycopg.connect(self.connectionString, autocommit=True)

    def connectAndDo(self, aCallback):
        return aCallback(self.connection)

    def execute(self, aCallback):
        with self.connection.cursor() as cursor:
            return aCallback(cursor)

    def userRepository(self):
        return PostgresUserRepository(self)

    def sessionRepository(self):
        return PostgresSessionRepository(self)
