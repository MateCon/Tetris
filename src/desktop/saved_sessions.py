from server_model.clock import Clock
from server.session_serialization import SessionDeserializer, SessionSerializer
import platformdirs
from pathlib import Path
from datetime import datetime, timedelta
import json
import os

from server_model.session import Session
from server_model.user import User


class SavedSessions:
    def __init__(self):
        self.sessions = []
        self.occupiedSessions = []

        self.loadSessions()

    def loadSessions(self):
        self.dataDir = platformdirs.user_data_path(appname="TetrisGame", appauthor="Mateo")

        if not self.dataDir.exists():
            self.dataDir.mkdir(parents=True)

        self.sessionsFile = self.dataDir.joinpath("sessions.json")
        if not self.sessionsFile.exists():
            self.sessionsFile.write_text("[]")

        try:
            content = json.loads(self.sessionsFile.read_text())
        except Exception:
            self.sessionsFile.write_text("[]")
            content = []

        for sessionDictionary in content:
            self.sessions.append(SessionDeserializer(sessionDictionary).deserialize())

    def saveSessions(self):
        self.sessionsFile.write_text(self.validSessionsToJson())

    def validSessionsToJson(self):
        currentTime = Clock().now()
        sessions = []

        for session in self.sessions:
            if session.expirationDate() > currentTime:
                sessions.append(SessionSerializer(session).serialize())

        return json.dumps(sessions)

    def add(self, aSession):
        self.sessions.append(aSession)
        self.saveSessions()

    def do(self, anAction):
        currentTime = Clock().now()

        for session in self.sessions:
            if session.expirationDate() > currentTime and not self.isUsing(session):
                anAction(session)

    def using(self, aSession):
        self.occupiedSessions.append(aSession)

    def stopUsing(self, aSession):
        self.occupiedSessions.remove(aSession)

    def isUsing(self, aSession):
        return aSession in self.occupiedSessions
