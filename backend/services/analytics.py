import sqlite3
from pathlib import Path
from datetime import datetime, timezone

class AnalyticsStore:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS analyses (
                analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                classification TEXT NOT NULL,
                password_length INTEGER NOT NULL,
                unique_character_ratio REAL NOT NULL,
                weakness_count INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS findings (
                finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER NOT NULL,
                finding_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (analysis_id) REFERENCES analyses(analysis_id)
            );
            """)

    def record_analysis(self, result):
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            cur = conn.execute("""
                INSERT INTO analyses
                (score, classification, password_length, unique_character_ratio, weakness_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                result["score"],
                result["classification"],
                result["metrics"]["length"],
                result["metrics"]["unique_character_ratio"],
                result["metrics"]["finding_count"],
                now,
            ))
            analysis_id = cur.lastrowid
            conn.executemany("""
                INSERT INTO findings (analysis_id, finding_type, severity, description)
                VALUES (?, ?, ?, ?)
            """, [
                (analysis_id, f["type"], f["severity"], f["description"])
                for f in result["findings"]
            ])

    def stats(self):
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
            avg = conn.execute("SELECT AVG(score) FROM analyses").fetchone()[0] or 0
            dist_rows = conn.execute("""
                SELECT classification, COUNT(*) AS count
                FROM analyses GROUP BY classification
            """).fetchall()
            score_rows = conn.execute("""
                SELECT score, COUNT(*) AS count
                FROM analyses GROUP BY score ORDER BY score
            """).fetchall()
            length_rows = conn.execute("""
                SELECT password_length, COUNT(*) AS count
                FROM analyses GROUP BY password_length ORDER BY password_length
            """).fetchall()

        distribution = {row["classification"]: row["count"] for row in dist_rows}
        for label in ("VERY WEAK", "WEAK", "MODERATE", "STRONG", "VERY STRONG"):
            distribution.setdefault(label, 0)

        return {
            "total_analyses": total,
            "average_score": round(avg, 2),
            "strength_distribution": distribution,
            "score_distribution": [dict(r) for r in score_rows],
            "length_distribution": [dict(r) for r in length_rows],
        }

    def weaknesses(self):
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT finding_type, COUNT(*) AS count
                FROM findings
                GROUP BY finding_type
                ORDER BY count DESC
            """).fetchall()
        return [dict(r) for r in rows]
