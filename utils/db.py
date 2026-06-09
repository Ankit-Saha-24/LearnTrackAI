import sqlite3

conn = sqlite3.connect(
    "database/learntrack.db",
    check_same_thread=False
)

cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Tasks Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    task TEXT,
    status TEXT
)
""")

# Study Progress Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS progress(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    subject TEXT,
    hours REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS placement_tracker(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    dsa INTEGER,
    aptitude INTEGER,
    projects INTEGER,
    interviews INTEGER
)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_tracker(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    study_hours INTEGER
)
""")

conn.commit()