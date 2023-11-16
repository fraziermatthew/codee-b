import sqlite3
con = sqlite3.connect("results.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE results (
        user_id TEXT NOT NULL UNIQUE PRIMARY KEY,
        user_input TEXT NOT NULL,
        model_output TEXT NOT NULL,
        q1 TEXT NOT NULL,
        q2 TEXT NOT NULL,
        q3 TEXT NOT NULL,
        q4 TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
""")