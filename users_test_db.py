import sqlite3
import random

# Connect to the existing GoGreen database
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()

# Insert a sample challenge (if not already there)
cursor.execute("INSERT OR IGNORE INTO challenges (challenge_id, challenge_name, points, description) VALUES (1, 'Recycle Bottles', 10, 'Recycle plastic bottles to earn points.')")

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
]

# Insert users and assign them points for challenge 1
for full_name, nickname, email, password in users:
    try:
        cursor.execute("INSERT INTO users (full_name, nickname, email, password) VALUES (?, ?, ?, ?)",
                       (full_name, nickname, email, password))
        user_id = cursor.lastrowid
        random_points = random.randint(5, 50)
        cursor.execute("INSERT INTO points (id, challenge_id, points) VALUES (?, 1, ?)", (user_id, random_points))
    except sqlite3.IntegrityError as e:
        print(f"Skipping {nickname} due to error: {e}")

conn.commit()
conn.close()

print("Sample users inserted successfully.")
