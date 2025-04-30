import sqlite3
import random

# Connect to the existing GoGreen database
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()

# Sample users to add
users = [
    ("Alice Johnson", "alicej", "alice@example.com", "pass123"),
    ("Bob Smith", "bobby", "bob@example.com", "pass123"),
    ("Charlie Lee", "charlie", "charlie@example.com", "pass123"),
    ("Diana Prince", "diana", "diana@example.com", "pass123" ),
    ("Ethan Hunt", "ethan", "ethan@example.com", "pass123"),
    ("Fiona Glen", "fiona", "fiona@example.com", "pass123"),
    ("George King", "george", "george@example.com", "pass123"),
    ("Hannah Ray", "hannah", "hannah@example.com", "pass123"),
    ("Ivan Novak", "ivan", "ivan@example.com", "pass123"),
    ("Julia Star", "julia", "julia@example.com", "pass123"),
    ("1", "1", "1", "1"),
]

for full_name, nickname, email, password in users:
    try:
        cursor.execute("INSERT INTO users (full_name, nickname, email, password) VALUES (?, ?, ?, ?)",
                       (full_name, nickname, email, password))
        user_id = cursor.lastrowid

    except sqlite3.IntegrityError as e:
        print(f"Skipping {nickname} due to error: {e}")


conn.commit()
conn.close()

print("Sample users inserted successfully.")
