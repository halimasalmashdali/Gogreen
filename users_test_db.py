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


import sqlite3
import random
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()
import sqlite3
import random
from datetime import datetime
import sqlite3
import random
from datetime import datetime


def test_insert_news_data():
    conn = sqlite3.connect("GoGreen.db")
    cursor = conn.cursor()

    # Sample data for news articles
    news_titles = [
        "New Tree Planting Initiative Launched",
        "Our Environmental Impact Over the Last Year",
        "Volunteer Program Success Stories",
        "Join Us for the Next Green Initiative Event",
        "Sustainability Goals Achieved in 2024"
    ]

    news_descriptions = [
        "We're excited to announce the launch of our new tree planting initiative that will help improve local green spaces and combat climate change.",
        "This year, we've planted over 1,000 trees across the city and are working hard to reduce our environmental footprint.",
        "Our volunteers have worked tirelessly on various community projects, making a real difference in our neighborhoods.",
        "Join us for an upcoming event where we focus on sustainable practices and community engagement for a greener future.",
        "This year, we have successfully achieved all of our sustainability goals, including reducing waste and increasing the use of renewable energy."
    ]

    author_names = [
        "Sophia Carter",
        "Liam Johnson",
        "Mia Davis",
        "Noah Walker",
        "Olivia Harris"
    ]

    # Insert sample news data into the news table
    for i in range(5):  # Insert 5 sample news articles
        title = random.choice(news_titles)
        description = random.choice(news_descriptions)
        author_name = random.choice(author_names)  # Simulate author names
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp for the news article

        cursor.execute('''
            INSERT INTO news (title, author_name, photo, text, date_created)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author_name, "default_photo.jpg", description, timestamp))

    # Commit changes and close the connection
    conn.commit()

    # Verifying if data is inserted
    cursor.execute("SELECT * FROM news")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

    print("Test news data added successfully!")


# Running the test function
test_insert_news_data()
