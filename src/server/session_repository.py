from server_model.database import SessionRepository
from server_model.session import Session
from server_model.user import User


class PostgresSessionRepository(SessionRepository):
    def __init__(self, aDatabase):
        self.database = aDatabase

    def insert(self, aSession):
        values = (aSession.id(), aSession.user().name(), aSession.creationDate(), aSession.duration())

        def query(cursor):
            cursor.execute("INSERT INTO session (id, user_name, creation_date, duration) VALUES (%s, %s, %s, %s)", values)

        self.database.execute(query)

    def find(self, anId) -> Session | None:
        def query(cursor):
            cursor.execute("SELECT * FROM session WHERE id=%s", (anId,))
            return cursor.fetchone()

        data = self.database.execute(query)

        return Session(data[0], User(data[1], ""), data[2], data[3])

