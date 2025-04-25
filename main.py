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
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT, 
                    nickname TEXT UNIQUE, 
                    email TEXT UNIQUE, 
                    password TEXT,
                    role TEXT)''')
cursor.execute('''DROP TABLE IF EXISTS challenges''')
cursor.execute('''CREATE TABLE IF NOT EXISTS challenges (
                    challenge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    challenge_name TEXT,
                    description TEXT,
                    points INTEGER,
                    completed BOOLEAN)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS points (
                    challenge_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (challenge_id) REFERENCES challenges(challenge_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS user_progress (
                    user_id INTEGER,
                    challenge_id INTEGER,
                    current_progress INTEGER DEFAULT 0,
                    target_progress INTEGER,
                    completed BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    FOREIGN KEY(challenge_id) REFERENCES challenges(challenge_id),
                    PRIMARY KEY(user_id, challenge_id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS trees (
                    tree_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tree_name TEXT,
                    tree_type TEXT,
                    description TEXT)''')
conn.close()

Window.size = (400, 600)


# Set the window size

class WelcomeScreen(Screen):
    pass


# Leaderboard start
class LeaderboardRow(BoxLayout):
    nickname = StringProperty()
    points = NumericProperty()
    bg_color = ListProperty([1, 1, 1, 1])


class LeaderboardScreen(Screen):
    def on_enter(self):
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('GoGreen.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nickname, COALESCE(SUM(p.points), 0) as total_points
            FROM users u
            LEFT JOIN points p ON u.id = p.id
            GROUP BY u.id
            ORDER BY total_points DESC
        ''')
        data = cursor.fetchall()
        conn.close()

        self.ids.leaderboard_list.clear_widgets()
        self.ids.top3_box.clear_widgets()

        # Top 3 display with colors
        top3_order = [1, 0, 2]  # Visually reorder to 2nd - 1st - 3rd
        top3_colors = [(1, 0.84, 0, 1), (0.75, 0.75, 0.75, 1), (0.8, 0.5, 0.2, 1)]
        top3_cards = []

        for i in range(min(3, len(data))):
            nickname, points = data[i]
            card = MDCard(
                orientation="vertical",
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                padding=dp(8),
                md_bg_color=top3_colors[i],
                radius=[12],
            )
            card.add_widget(MDLabel(text=nickname, halign="center", theme_text_color="Primary", ))
            card.add_widget(MDLabel(text=f"{points} pts", halign="center", theme_text_color="Secondary"))
            top3_cards.append(card)

        for i, idx in enumerate(top3_order):
            if idx < len(top3_cards):
                self.ids.top3_box.add_widget(top3_cards[idx])
                if i < len(top3_order) - 1:
                    self.ids.top3_box.add_widget(Widget(size_hint_x=None, width=dp(2)))

        # Remaining users (4th place onwards)
        for i, (nickname, points) in enumerate(data[3:], start=4):
            row = LeaderboardRow(
                nickname=nickname,
                points=points,
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
            cursor.execute("INSERT INTO points (points) VALUES (0)")
            conn.commit()
            print("User registered successfully!")

            # Redirect to homepage
            self.manager.current = "homepage"

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

class ChallengesScreen(Screen):
    def default_challenges(self):
        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM challenges")
            cursor.execute(''' 
                INSERT INTO challenges(challenge_name, description, points, completed) VALUES
                    ("Use Reusable Bags", "Use reusable shopping bags 5 times", 10, FALSE),
                    ("Take Care Of A Plant", "Water a Plant for a month", 20, FALSE),
                    ("Lights Off", "Turn off unused lights 15 times", 5, FALSE),
                    ("Avoid Plastic Bags", "Avoid using plastic bags for shopping 3 times", 10, FALSE),
                    ("Recycle Plastic", "Put 20 plastic materials you find into recycle bins", 30, FALSE),
                    ("Public Transport", "Use public transportation 5 times", 20, FALSE),
                    ("Use Less Water", "Turn off running water 15 times", 10, FALSE),
                    ("Plant A Plant", "Plant any type of plant and take care of it for a month", 50, FALSE),
                    ("Use Reusable Bottles", "Do not purchase or use plastic bottles for a month", 5, FALSE),
                    ("Don't Use Plastic", "Avoid the usage of any plastic materials for a week", 20, FALSE)
            ''')
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def on_enter(self):
        # Prevent duplicate loading
        if hasattr(self, 'content_added') and self.content_added:
            return

        grid = self.ids.content_area

        conn = sqlite3.connect("GoGreen.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT challenge_name, description, points FROM challenges")
            for row in cursor:
                name = row["challenge_name"]
                desc = row["description"]
                points = row["points"]

                btn = Button(
                    text=f"{name}\n{points} pts",
                    size_hint=(1, None),
                    height=dp(100),
                    background_normal="",
                    background_color=(0, 0.6 + random() / 4, 0.6 + random() / 4, 1),
                    color=(1, 1, 1, 1),
                    font_size="12sp",
                    bold=True
                )
                btn.bind(on_press=partial(self.open_challenge_detail, name, desc, points))
                grid.add_widget(btn)

            self.content_added = True

        finally:
            cursor.close()
            conn.close()

    def open_challenge_detail(self, name, description, points, instance):
        detail_screen = self.manager.get_screen('challenge_detail')
        detail_screen.set_challenge(name, description, points)
        self.manager.current = 'challenge_detail'

    def load_challenges(self):
        from kivy.uix.label import Label
        import sqlite3

        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT challenge_name, description FROM challenges WHERE completed = 0")
        challenges = cursor.fetchall()
        cursor.close()
        conn.close()

        content_area = self.ids.content_area
        content_area.clear_widgets()

        for name, desc in challenges:
            content_area.add_widget(
                Label(text=f"[b]{name}[/b]\n{desc}", markup=True, size_hint_y=None, height=100))

class ChallengeDetailScreen(Screen):
    def set_challenge(self, name, description, points):
        self.ids.challenge_name.text = name
        self.ids.challenge_desc.text = description
        self.ids.challenge_points.text = f"Points: {points}"
        self.ids.challenge_progress.value = 0
        self.event = Clock.schedule_interval(self.update_progress, 1 / 25)

    def update_progress(self, dt):
        pb = self.ids.challenge_progress
        if pb.value < 100:
            pb.value += 1
        else:
            Clock.unschedule(self.event)

    def on_leave(self):
        # Stop progress when leaving screen
        if hasattr(self, 'event'):
            Clock.unschedule(self.event)


# Challenges finish

# Map start
class MapScreen(Screen):
    def on_start(self):
        marker = MapMarkerPopup(lat=41, lon=69)
        self.root.add_widget(marker)


# Map finish

# Profile start
class ProfileScreen(Screen):
    def on_enter(self):
        self.load_user_challenges()

    # ProfileScreen load_user_challenges method
    def load_user_challenges(self):
        nickname = App.get_running_app().current_user_nickname
        conn = sqlite3.connect("GoGreen.db")
        cursor = conn.cursor()

        cursor.execute(""" 
            SELECT c.challenge_name, c.description, p.points
            FROM users u
            JOIN points p ON u.id = p.id
            JOIN challenges c ON p.challenge_id = c.challenge_id
            WHERE u.nickname = ? 
        """, (nickname,))
        data = cursor.fetchall()
        conn.close()

        container = self.ids.challenges_container
        container.clear_widgets()

        if not data:
            # Create a BoxLayout to ensure horizontal alignment
            no_challenges_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(140))

            # Create MDLabel for "No active challenges"
            label = MDLabel(
                text="No active challenges",
                halign="center",
                theme_text_color="Custom",
                text_color=(0.5, 0.5, 0.5, 1),
                font_style="Body1",
                size_hint=(None, None),
                size=(dp(200), dp(40)),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )

            # Add label to the layout and layout to the container
            no_challenges_layout.add_widget(label)
            container.add_widget(no_challenges_layout)
        else:
            # Add challenges to the container as usual
            for name, description, points in data:
                card = MDCard(
                    orientation="vertical",
                    padding=dp(10),
                    size_hint=(None, None),
                    size=(dp(120), dp(100)),
                    radius=[12],
                    md_bg_color=(0.7, 1, 0.7, 1),
                    ripple_behavior=True,
                )
                card.bind(on_release=partial(self.open_challenge, name, description, points))

                card.add_widget(MDLabel(text=name, bold=True, font_style="H6", halign="center"))
                card.add_widget(MDLabel(text=f"{points} pts", theme_text_color="Secondary", halign="center"))
                container.add_widget(card)

    def open_challenge(self, name, description, points, instance):
        detail_screen = self.manager.get_screen("challenge_detail")
        detail_screen.set_challenge(name, description, points)
        self.manager.current = "challenge_detail"

    def congs(self, instance):
        self.manager.current = "settings"


# Profile finish


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
        Builder.load_file("screens/challenges_screen.kv")  # challenges .kv file
        Builder.load_file("screens/map_screen.kv")  # map .kv file
        Builder.load_file("screens/profile_screen.kv")  # profile .kv file
        Builder.load_file("screens/challenge_details_screen.kv")  # challenge details .kv file

        ChallengesScreen().default_challenges()
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
        sm.add_widget(ChallengesScreen(name="challenges"))
        sm.add_widget(ChallengeDetailScreen(name="challenge_detail"))

        sm.current = "welcome"  # Start with WelcomeScreen
        return sm

    def leaderboard_page(self):
        self.root.current = "leaderboard"

    def home_page(self):
        self.root.current = "homepage"

    def challenges_page(self):
        self.root.current = "challenges"

    def map_page(self):
        self.root.current = "map"

    def profile_page(self):
        self.root.current = "profile"


if __name__ == "__main__":
    GoGreenApp().run()
