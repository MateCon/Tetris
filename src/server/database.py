import psycopg
from psycopg_pool import ConnectionPool
from server.user_repository import PostgresUserRepository
from server.session_repository import PostgresSessionRepository
from server_model.database import Database


class PostgresDatabase(Database):
    def __init__(self, aConnectionString):
        self.connectionString = aConnectionString
        self.pool = ConnectionPool(self.connectionString, min_size=1, max_size=10)

    def execute(self, aCallback):
        with self.pool.connection() as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                return aCallback(cursor)

    def userRepository(self):
        return PostgresUserRepository(self)

    def sessionRepository(self):
        return PostgresSessionRepository(self)
