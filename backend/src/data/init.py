"""Initialize SQLite database"""

from pathlib import Path
from sqlite3 import connect, Connection, Cursor
import os

class Database:
    def __init__(self, db_name: str | None = None):
        self.conn: Connection | None = None
        self.curs: Cursor | None = None
        self.db_name = db_name or self._get_default_db_name()

    def _get_default_db_name(self) -> str:
        top_dir = Path(__file__).resolve().parents[1]  # repo top
        db_dir = top_dir / "db"
        db_name = "todo.db"
        db_path = str(db_dir / db_name)
        return os.getenv("TODO_SQLITE_DB", db_path)

    def connect(self, reset: bool = False):
        if self.conn and not reset:
            return
        if self.conn:
            self.close()
        self.conn = connect(self.db_name, check_same_thread=False)
        self.curs = self.conn.cursor()

    def close(self):
        if self.curs:
            self.curs.close()
        if self.conn:
            self.conn.close()
        self.conn = None
        self.curs = None

    def execute(self, query: str, params: tuple = ()):
        if not self.conn:
            self.connect()
        self.curs.execute(query, params)
        self.conn.commit()
        return self.curs

    def fetchall(self) -> list:
        return self.curs.fetchall()

    def fetchone(self):
        return self.curs.fetchone()

    def lastrowid(self):
        return self.curs.lastrowid


db = Database()
db.connect()