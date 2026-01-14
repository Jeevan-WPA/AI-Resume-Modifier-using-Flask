import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            job_title TEXT,
            location TEXT,
            date_applied TEXT,
            url TEXT,
            pdf_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_job(job_details):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO jobs (company, job_title, location, date_applied, url, pdf_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_details.get("company", ""),
        job_details.get("job_title", ""),
        job_details.get("location", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        job_details.get("url", ""),
        job_details.get("pdf_path", "")
    ))
    conn.commit()
    conn.close()

def get_jobs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs ORDER BY date_applied DESC")
    rows = c.fetchall()
    conn.close()
    return rows
