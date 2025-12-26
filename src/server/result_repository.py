from server_model.database import ResultRepository


class PostgresResultRepository(ResultRepository):
    def __init__(self, aDatabase):
        self.database = aDatabase

    def insert(self, aUserName, aScore, aLevel, anAmmountOfLines, aCreationDate, aTimeInMilliseconds):
        values = (aUserName, aScore, aLevel, anAmmountOfLines, aCreationDate, aTimeInMilliseconds)

        def query(cursor):
            cursor.execute("INSERT INTO result (user_name, score, last_level, lines, creation_date, time_of_play) VALUES (%s, %s, %s, %s, %s, %s)", values)

        self.database.execute(query)
