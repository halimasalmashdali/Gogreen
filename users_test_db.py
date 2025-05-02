# import sqlite3
# import random
#
# # Connect to the existing GoGreen database
# conn = sqlite3.connect("GoGreen.db")
# cursor = conn.cursor()
#
# # Sample users to add
# users = [
#     ("Alice Johnson", "alicej", "alice@example.com", "pass123"),
#     ("Bob Smith", "bobby", "bob@example.com", "pass123"),
#     ("Charlie Lee", "charlie", "charlie@example.com", "pass123"),
#     ("Diana Prince", "diana", "diana@example.com", "pass123" ),
#     ("Ethan Hunt", "ethan", "ethan@example.com", "pass123"),
#     ("Fiona Glen", "fiona", "fiona@example.com", "pass123"),
#     ("George King", "george", "george@example.com", "pass123"),
#     ("Hannah Ray", "hannah", "hannah@example.com", "pass123"),
#     ("Ivan Novak", "ivan", "ivan@example.com", "pass123"),
#     ("Julia Star", "julia", "julia@example.com", "pass123"),
#     ("1", "1", "1", "1"),
# ]
#
# for full_name, nickname, email, password in users:
#     try:
#         cursor.execute("INSERT INTO users (full_name, nickname, email, password) VALUES (?, ?, ?, ?)",
#                        (full_name, nickname, email, password))
#         user_id = cursor.lastrowid
#
#     except sqlite3.IntegrityError as e:
#         print(f"Skipping {nickname} due to error: {e}")
#
#
# conn.commit()
# conn.close()
#
# print("Sample users inserted successfully.")



import sqlite3
import random

# Connect to the GoGreen database
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()

# Step 1: Alter the table if not already done
try:
    cursor.execute("ALTER TABLE trees ADD COLUMN name TEXT")
except sqlite3.OperationalError:
    print("Column 'name' already exists.")

try:
    cursor.execute("ALTER TABLE trees ADD COLUMN species TEXT")
except sqlite3.OperationalError:
    print("Column 'species' already exists.")

# Step 2: Get all user IDs
cursor.execute("SELECT user_id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

# Step 3: Tree data
tree_names = [
    "Oak Tree", "Maple Tree", "Pine Tree", "Birch Tree", "Cedar Tree",
    "Cherry Tree", "Apple Tree", "Palm Tree", "Spruce Tree", "Willow Tree"
]
species_list = [
    "Quercus", "Acer", "Pinus", "Betula", "Cedrus",
    "Prunus", "Malus", "Arecaceae", "Picea", "Salix"
]
descriptions = [
    "Planted during Arbor Day event.",
    "Grown near the city park.",
    "Decorated with lights during winter.",
    "Part of the urban greening project.",
    "Provides a lot of shade.",
    "Fruits are harvested yearly.",
    "Near the school entrance.",
    "Survived last year's storm.",
    "Young but growing fast.",
    "Symbolic tree for our community."
]

# Step 4: Insert sample trees
for i in range(10):
    name = tree_names[i]
    species = species_list[i]
    desc = descriptions[i]
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    user_id = random.choice(user_ids)

    try:
        cursor.execute(
            "INSERT INTO trees (name, species, user_id, desc, lat, lon) VALUES (?, ?, ?, ?, ?, ?)",
            (name, species, user_id, desc, lat, lon)
        )
    except sqlite3.Error as e:
        print(f"Error inserting tree {name}: {e}")

conn.commit()
conn.close()

print("Sample trees inserted successfully.")
