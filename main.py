import sqlite3
from functools import partial

# all kivy imports
from kivy.uix.boxlayout import BoxLayout
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

    c.execute('INSERT INTO trees (user_id, name, lat, lon, desc) VALUES (?, ?, ?, ?, ?)',
              (user_id, name, lat, lon, description))

    conn.commit()
    conn.close()
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

class HomepageScreen(Screen):
    pass


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

# Challenges start
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import dp
from functools import partial
import sqlite3
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


# Challenges finish
import sqlite3
import sqlite3
import random
#
# # Connect to the database
# conn = sqlite3.connect("GoGreen.db")
# cursor = conn.cursor()
#
# # Example user IDs (must exist in your users table)
# user_ids = [1, 2]  # Replace with actual user IDs from your database
#
# # Sample tree descriptions
# descriptions = [
#     "Oak tree planted in community park",
#     "Maple tree near downtown",
#     "Pine tree in residential area",
#     "Fruit tree in school garden",
#     "Willow tree by the riverbank",
#     "Redwood tree in conservation area",
#     "Birch tree in urban plaza"
# ]
#
# # Generate realistic coordinates within a city area (example: San Francisco)
# def generate_coordinates():
#     # Base coordinates (SF area)
#     base_lat = 37.7749
#     base_lon = -122.4194
#     # Random variation (about 10km radius)
#     lat_variation = random.uniform(-0.1, 0.1)
#     lon_variation = random.uniform(-0.1, 0.1)
#     return (base_lat + lat_variation, base_lon + lon_variation)
#
# # Insert 20 example trees
# cursor.execute("SELECT COUNT(*) FROM trees")
# tree_count = cursor.fetchone()[0]
#
# if tree_count == 0:
#     # Insert 20 example trees
#     for i in range(20):
#         user_id = random.choice(user_ids)
#         description = random.choice(descriptions)
#         lat, lon = generate_coordinates()
#
#         cursor.execute('''
#             INSERT INTO trees (user_id, desc, lat, lon)
#             VALUES (?, ?, ?, ?)
#         ''', (user_id, description, lat, lon))
#
#
# # Commit changes and close connection
# conn.commit()
# conn.close()


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

                content = BoxLayout(orientation='vertical', size=(200, 100))
                content.add_widget(Button(
                    text="Details",
                    size_hint_y=None,
                    height=40
                ))
                marker.add_widget(content)

                mapview.add_marker(marker)

            if trees:
                mapview.center_on(trees[0]['lat'], trees[0]['lon'])
                mapview.zoom = 3

        except Exception as e:
            print(f"Error loading map: {e}")
        finally:
            cursor.close()
            conn.close()
# Map finish


from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import random

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import random

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import sqlite3


from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class TreeCard(BoxLayout):
    def __init__(self, name, lat, lon, tree_id, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = 120
        self.spacing = 5

        self.tree_id = tree_id

        self.name_label = Label(text=f"{name}", font_size=18)
        self.lat_label = Label(text=f"Latitude: {lat}", font_size=14)
        self.lon_label = Label(text=f"Longitude: {lon}", font_size=14)

        self.details_button = Button(text="View Details", size_hint_y=None, height=40)
        self.details_button.bind(on_press=self.on_details_button_pressed)

        self.add_widget(self.name_label)
        self.add_widget(self.lat_label)
        self.add_widget(self.lon_label)
        self.add_widget(self.details_button)

    def on_details_button_pressed(self, instance):
        self.parent.parent.view_tree_details(self.tree_id)



from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

class ProfileScreen(Screen):
    def on_enter(self):
        self.display_user_trees()

        app = App.get_running_app()
        nickname = app.current_user_nickname

        # Fetch user ID
        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE nickname = ?", (nickname,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            cursor.execute("SELECT COUNT(*) FROM trees WHERE user_id = ?", (user_id,))
            tree_count = cursor.fetchone()[0]
            self.ids.user_tree_label.text = f"{nickname}, you have {tree_count} registered trees"
        else:
            self.ids.user_tree_label.text = "User not found."

        conn.close()

    def display_user_trees(self):
        app = App.get_running_app()
        nickname = app.current_user_nickname
        user_id = get_user_id_by_nickname(nickname)

        if not user_id:
            print("User ID not found.")
            return

        trees = fetch_user_trees(user_id)

        tree_list = self.ids.tree_list
        tree_list.clear_widgets()

        for tree in trees:
            tree_card = MDCard(
                orientation="vertical",
                padding=dp(10),
                size_hint_y=None,
                height=dp(80),
                md_bg_color=(0.9, 1, 0.9, 1),
                radius=[8],
            )
            tree_card.add_widget(MDLabel(text=f"🌳 {tree[2]}", halign="left", theme_text_color="Primary"))  # name
            tree_card.add_widget(MDLabel(text=f"📍 {tree[5]}, {tree[6]}", halign="left", theme_text_color="Secondary"))  # lat/lon
            tree_card.add_widget(MDLabel(text=f"📝 {tree[4]}", halign="left", theme_text_color="Secondary"))  # desc

            tree_list.add_widget(tree_card)

# Profile finish


#Tree registration start
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

        # Call your existing tree registration function here
        add_tree(App.get_running_app().current_user_nickname, name, lat, lon, description)  # This should be your existing function to add the tree
        print(App.get_running_app().current_user_nickname)
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


        # need to add settings
        # need to add screens for solo challenges

        # Create ScreenManager and add widgets/screens
        sm = MDScreenManager()

        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(HomepageScreen(name="homepage"))
        sm.add_widget(LeaderboardScreen(name="leaderboard"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(MapScreen(name="map"))
        sm.add_widget(TreeRegistrationScreen(name="tree_reg"))



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
