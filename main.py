import sqlite3
from functools import partial

from kivy.core.image import Image
# all kivy imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivymd.uix.button import MDRaisedButton

global current_user_nickname

# imports for map
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapSource, MapMarkerPopup

# imports for challenges
from random import random

# all kivymd imports
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel

# Set the window size
Window.size = (400, 600)

# Database setup
import sqlite3


def get_user_id_by_nickname(nickname):
    conn = sqlite3.connect("GoGreen.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE nickname = ?", (nickname,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Connect to the database
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()

# Create 'users' table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT, 
                    nickname TEXT UNIQUE, 
                    email TEXT UNIQUE, 
                    password TEXT,
                    role TEXT)''')

# Create 'trees' table
cursor.execute('''CREATE TABLE IF NOT EXISTS trees (
                    tree_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    species TEXT,
                    desc TEXT,
                    lat REAL,
                    lon REAL,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')

# Create news table

cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author_name TEXT,
                    photo TEXT,
                    text TEXT,
                    date_created TEXT)''')


def fetch_user_trees(user_id):
    conn = sqlite3.connect('GoGreen.db')
    c = conn.cursor()

    c.execute('SELECT * FROM trees WHERE user_id = ?', (user_id,))
    trees = c.fetchall()

    conn.close()
    return trees


def add_tree(user_id, name, lat, lon, description):
    conn = sqlite3.connect('GoGreen.db')
    c = conn.cursor()

    # Insert the tree data into the database
    c.execute('INSERT INTO trees (user_id, name, lat, lon, desc) VALUES (?, ?, ?, ?, ?)',
              (user_id, name, lat, lon, description))

    conn.commit()  # Ensure the transaction is saved
    conn.close()

    # Debugging: log the insertion
    print(f"Added tree: {name} at ({lat}, {lon}) for user {user_id}")


# Enable foreign key constraints (ensure that foreign keys work)
cursor.execute('PRAGMA foreign_keys = ON')

# Commit the changes and close the connection
conn.commit()
conn.close()

Window.size = (400, 600)


# Set the window size

class WelcomeScreen(Screen):
    pass


# Leaderboard start
class LeaderboardRow(BoxLayout):
    nickname = StringProperty()
    trees_planted = NumericProperty()
    bg_color = ListProperty([1, 1, 1, 1])


class LeaderboardScreen(Screen):
    def on_enter(self):
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('GoGreen.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nickname, COUNT(t.tree_id) as total_trees
            FROM users u
            LEFT JOIN trees t ON u.user_id = t.user_id
            GROUP BY u.user_id
            ORDER BY total_trees DESC
        ''')
        data = cursor.fetchall()
        conn.close()

        self.ids.leaderboard_list.clear_widgets()
        self.ids.top3_box.clear_widgets()

        # Top 3 display with colors
        top3_order = [1, 0, 2]  # Show 2nd, then 1st, then 3rd for visual effect
        top3_colors = [(1, 0.84, 0, 1), (0.75, 0.75, 0.75, 1), (0.8, 0.5, 0.2, 1)]
        top3_cards = []

        for i in range(min(3, len(data))):
            nickname, trees = data[i]
            card = MDCard(
                orientation="vertical",
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                padding=dp(8),
                md_bg_color=top3_colors[i],
                radius=[12],
            )
            card.add_widget(MDLabel(text=nickname, halign="center", theme_text_color="Primary"))
            card.add_widget(MDLabel(text=f"{trees} trees", halign="center", theme_text_color="Secondary"))
            top3_cards.append(card)

        for i, idx in enumerate(top3_order):
            if idx < len(top3_cards):
                self.ids.top3_box.add_widget(top3_cards[idx])
                if i < len(top3_order) - 1:
                    self.ids.top3_box.add_widget(Widget(size_hint_x=None, width=dp(2)))

        # Remaining users
        for i, (nickname, trees) in enumerate(data[3:], start=4):
            row = LeaderboardRow(
                nickname=nickname,
                trees_planted=trees,
                bg_color=(0.8, 1, 0.8, 1) if App.get_running_app().current_user_nickname == nickname else (1, 1, 1, 1)
            )
            self.ids.leaderboard_list.add_widget(row)


# Leaderboard finish

# Homepage start
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.uix.button import Button
from functools import partial
import sqlite3
from kivy.uix.screenmanager import Screen

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from functools import partial
import sqlite3



class NewsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Delay loading data until layout is ready
        self.bind(on_enter=self.load_news)

    def load_news(self, *args):
        self.ids.news_box.clear_widgets()
        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT id, title, text, author_name, date_created FROM news''')
        news_data = cursor.fetchall()
        conn.close()

        for row in news_data:
            news_id, title, description, author, timestamp = row
            desc_trunc = description[:30] + '...'
            button = Button(
                text=f"[b]{title}[/b]\n[i]Author: {author}[/i]\n{desc_trunc}",
                size_hint_y=None,
                height=100,
                on_press=partial(self.on_news_click, news_id),
                markup=True,
                background_normal='',
                background_color=(0.2, 0.6, 0.2, 1),
                color=(1, 1, 1, 1),
                font_size=16,
                padding=[10, 10],
            )
            self.ids.news_box.add_widget(button)

    def on_news_click(self, news_id, *args):
        self.manager.get_screen('news_detail').load_news_detail(news_id)
        self.manager.current = 'news_detail'


from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import sqlite3


class NewsDetailScreen(Screen):
    news_title = StringProperty("Loading...")
    news_description = StringProperty("Loading...")
    news_author = StringProperty("Unknown Author")
    news_timestamp = StringProperty("Unknown Date")

    def load_news_detail(self, news_id):
        # Debugging: Check the news_id that is passed
        print(f"Loading detail for news_id: {news_id}")

        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, text, author_name, date_created FROM news WHERE id=?", (news_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            title, text, author, date_created = row
            self.news_title = title
            self.news_description = text
            self.news_author = f"By: {author}"
            self.news_timestamp = date_created
        else:
            self.news_title = "News Not Found"
            self.news_description = ""
            self.news_author = ""
            self.news_timestamp = ""


# Homepage finish

# Register start
class RegisterScreen(Screen):
    def register(self):
        full_name = self.ids.full_name.text
        nickname = self.ids.nickname.text
        email = self.ids.email.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text

        if not full_name or not nickname or not email or not password:
            print("All fields are required!")
            return

        if password != confirm_password:
            print("Passwords do not match!")
            return

        conn = sqlite3.connect("Gogreen.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (full_name, nickname, email, password) VALUES (?, ?, ?, ?)",
                           (full_name, nickname, email, password))
            conn.commit()
            print("User registered successfully!")
            app = App.get_running_app()
            app.current_user_nickname = nickname  # Store the current user's nickname

            self.manager.current = "profile"

        except sqlite3.IntegrityError:
            print("Nickname or email already exists!")
        finally:
            conn.close()


# Register finish

# Login start
class LoginScreen(Screen):
    def login(self):
        login_input = self.ids.login_input.text
        password = self.ids.password.text

        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE (email=? OR nickname=?) AND password=?",
                       (login_input, login_input, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            print("Login successful!")
            App.get_running_app().current_user_nickname = user[2]
            # Redirect to homepage
            self.manager.current = "homepage"

        else:
            print("Invalid email/nickname or password!")


# Login finish


# Map start
class MapScreen(Screen):
    def on_enter(self):
        mapview = self.ids.mapview
        conn = sqlite3.connect("GoGreen.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT lat, lon FROM trees")
            trees = cursor.fetchall()
            print(f"Loaded {len(trees)} trees")

            for tree in trees:
                marker = MapMarkerPopup(
                    lat=tree['lat'],
                    lon=tree['lon'],
                    source='assets/photos/tree_icon.png'
                )
                marker.size_hint = (None, None)
                marker.size = (30, 30)
                print('working 1')
                content = BoxLayout(orientation='vertical', size=(200, 100))
                content.add_widget(Button(
                    text="Details",
                    size_hint_y=None,
                    height=40
                ))
                marker.add_widget(content)

                mapview.add_marker(marker)
                print('working 2')
            if trees:
                print('working 3')
                mapview.center_on(trees[0]['lat'], trees[0]['lon'])
                mapview.zoom = 3
                print('working 4')
        except Exception as e:
            print(f"Error loading map: {e}")
        finally:
            cursor.close()
            conn.close()


# Map finish


from kivy.uix.widget import Widget
import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


class ProfileScreen(Screen):
    def on_enter(self):
        self.load_user_trees()

    def load_user_trees(self):
        app = App.get_running_app()
        user_id = get_user_id_by_nickname(app.current_user_nickname)  # Get user ID from nickname
        if user_id:  # Ensure user_id is valid
            trees = fetch_user_trees(user_id)  # Fetch trees for the user
            tree_list = self.ids.tree_list  # Ensure you have a tree_list in your kv file
            tree_list.clear_widgets()  # Clear existing widgets before adding new ones
            print(trees)
            for tree in trees:
                tree_card = MDCard(
                    orientation="vertical",
                    padding=dp(10),
                    size_hint_y=None,
                    height=dp(80),
                    md_bg_color=(0.9, 1, 0.9, 1),  # Set background color
                    radius=[8],  # Rounded corners
                )
                tree_card.add_widget(
                    MDLabel(text=f"🌳 {tree[2]}", halign="left", theme_text_color="Primary"))  # Tree name
                tree_card.add_widget(MDLabel(text=f"📍 {tree[5]}, {tree[6]}", halign="left"))  # Location

                tree_list.add_widget(tree_card)  # Add the tree card to the UI


# Profile finish


# Tree registration start
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class TreeRegistrationScreen(Screen):
    def register_tree(self):
        name = self.ids.name.text
        lat = float(self.ids.lat.text)
        lon = float(self.ids.lan.text)
        description = self.ids.desc.text

        conn = sqlite3.connect('GoGreen.db')
        c = conn.cursor()

        # Get the user ID based on the current user's nickname
        c.execute('SELECT user_id FROM users WHERE nickname = ?', (App.get_running_app().current_user_nickname,))
        user_id = c.fetchone()

        if user_id is None:
            print("User not found!")
            return

        user_id = user_id[0]  # Extract the user_id from the query result

        # Insert the tree data into the database
        c.execute('INSERT INTO trees (user_id, name, lat, lon, desc) VALUES (?, ?, ?, ?, ?)',
                  (user_id, name, lat, lon, description))

        conn.commit()  # Ensure the transaction is saved
        conn.close()

        # Go back to profile screen
        self.manager.current = 'profile'


# Tree registration end


# MAIN APP
class GoGreenApp(MDApp):
    current_user_nickname = None

    def build(self):
        # Initialize the app first
        self.theme_cls.primary_palette = "Green"  # change the theme if needed

        # Load the KV file after app initialization
        Builder.load_file("screens/welcome_screen.kv")  # welcome .kv file
        Builder.load_file("screens/reg_screen.kv")  # registration .kv file
        Builder.load_file("screens/login_screen.kv")  # login .kv file
        Builder.load_file("screens/home_screen.kv")  # home .kv file
        Builder.load_file("screens/leaderboard_screen.kv")  # leaderboard .kv file
        Builder.load_file("screens/treetracker_screen.kv")  # tracker .kv file
        Builder.load_file("screens/map_screen.kv")  # map .kv file
        Builder.load_file("screens/profile_screen.kv")  # profile .kv file
        Builder.load_file("screens/news_detail.kv")  # details .kv file

        # need to add settings
        # need to add screens for solo challenges

        # Create ScreenManager and add widgets/screens
        sm = MDScreenManager()

        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(LeaderboardScreen(name="leaderboard"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(MapScreen(name="map"))
        sm.add_widget(TreeRegistrationScreen(name="tree_reg"))
        sm.add_widget(NewsScreen(name="homepage"))
        sm.add_widget(NewsDetailScreen(name="news_detail"))

        sm.current = "welcome"  # Start with WelcomeScreen
        return sm

    def leaderboard_page(self):
        self.root.current = "leaderboard"

    def tree_reg_page(self):
        self.root.current = "tree_reg"

    def home_page(self):
        self.root.current = "homepage"

    def map_page(self):
        self.root.current = "map"

    def profile_page(self):
        self.root.current = "profile"


if __name__ == "__main__":
    GoGreenApp().run()
