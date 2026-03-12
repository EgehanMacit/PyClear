import sqlite3
import json
import os

DB_FILE = "pyclear_history.db"

class DBManager:
    def __init__(self):
        os.makedirs("db", exist_ok=True)
        self.conn = sqlite3.connect(os.path.join("db", DB_FILE))
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT,
                result_json TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_record(self, file_path, result_data):
        """Add analysis result to DB"""
        result_json = json.dumps(result_data)
        self.cursor.execute(
            "INSERT INTO history (file_path, result_json) VALUES (?, ?)",
            (file_path, result_json)
        )
        self.conn.commit()

    def get_history(self):
        """Return all history entries as list of dicts"""
        self.cursor.execute("SELECT id, file_path, result_json, timestamp FROM history ORDER BY timestamp DESC")
        rows = self.cursor.fetchall()
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "file_path": row[1],
                "result_data": json.loads(row[2]),
                "timestamp": row[3]
            })
        return history
