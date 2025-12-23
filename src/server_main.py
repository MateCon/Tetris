from flask import Flask
from server.database import PostgresDatabase
from server.setup_application import SetupFlaskApplication
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
db = PostgresDatabase(os.getenv("DB_CONNECTION_STRING"))
SetupFlaskApplication(app, db).setup()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, ssl_context=("ssl/server.crt", "ssl/server.key"))
