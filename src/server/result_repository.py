from server_model.database import ResultRepository
from server_model.game_result import GameResult
from server_model.user import User


class PostgresResultRepository(ResultRepository):
    def __init__(self, aDatabase):
        self.database = aDatabase

    def insert(self, aGameResult):
        values = (
            aGameResult.user.name(),
            aGameResult.score,
            aGameResult.level,
            aGameResult.lines,
            aGameResult.creationDate,
            aGameResult.time
        )

        def query(cursor):
            cursor.execute("INSERT INTO result (user_name, score, last_level, lines, creation_date, time_of_play) VALUES (%s, %s, %s, %s, %s, %s)", values)

        self.database.execute(query)

    def selectAll(self):
        def query(cursor):
            cursor.execute("SELECT * FROM result")
            return cursor.fetchall()

        rows = self.database.execute(query)

        users = []
        for row in rows:
            users.append(GameResult(User(row[0], ""), row[1], row[2], row[3], row[4], row[5]))

        return users
