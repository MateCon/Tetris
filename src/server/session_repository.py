from server_model.database import SessionRepository


class PostgresSessionRepository(SessionRepository):
    def __init__(self, aDatabase):
        self.database = aDatabase

    def insert(self, aSession):
        values = (aSession.id(), aSession.user().name(), aSession.creationDate(), aSession.duration())

        def query(cursor):
            cursor.execute("INSERT INTO session (id, user_name, creation_date, duration) VALUES (%s, %s, %s, %s)", values)

        self.database.execute(query)
