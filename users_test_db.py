import sqlite3
import random

conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()

# Sample data for users
user_data = [
    ("Alice Johnson", "alicej", "alice@example.com", "pass123", "user"),
    ("Bob Smith", "bobster", "bob@example.com", "pass456", "user"),
    ("Charlie Lee", "chazzy", "charlie@example.com", "charlie789", "admin"),
    ("Dana Kim", "danak", "dana@example.com", "dkpassword", "user"),
    ("Eli Turner", "elturn", "eli@example.com", "mypw123", "moderator")
]

# Insert users
for full_name, nickname, email, password, role in user_data:
    cursor.execute('''
        INSERT OR IGNORE INTO users (full_name, nickname, email, password, role)
        VALUES (?, ?, ?, ?, ?)
    ''', (full_name, nickname, email, password, role))

# Get all user_ids
cursor.execute("SELECT user_id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

# Sample tree species and names
tree_species = ["Oak", "Maple", "Birch", "Pine", "Cedar"]
tree_names = ["Greenie", "Leafy", "TallBoy", "ShadeMaster", "Branchy"]

# Insert trees
for _ in range(10):  # 10 sample trees
    user_id = random.choice(user_ids)
    name = random.choice(tree_names)
    species = random.choice(tree_species)
    desc = f"A beautiful {species} tree named {name}"
    lat = round(random.uniform(-90.0, 90.0), 6)
    lon = round(random.uniform(-180.0, 180.0), 6)
    cursor.execute('''
        INSERT INTO trees (user_id, name, species, desc, lat, lon)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, name, species, desc, lat, lon))

conn.commit()
conn.close()
