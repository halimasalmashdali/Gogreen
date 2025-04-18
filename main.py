import sqlite3
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screenmanager import MDScreenManager


# Set the window size
Window.size = (400, 600)

# Database setup
conn = sqlite3.connect("GoGreen.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT, 
                    nickname TEXT UNIQUE, 
                    email TEXT UNIQUE, 
                    password TEXT,
                    role TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS challenges (
                    challenge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    challenge_name TEXT,
                    points INTEGER, 
                    description TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS points(
                    id INTEGER,
                    challenge_id INTEGER,
                    points INTEGER,
                    FOREIGN KEY (id) REFERENCES users(id),
                    FOREIGN KEY (challenge_id) REFERENCES challenges(challenge_id))''')
conn.commit()
conn.close()


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window

# Set the window size
Window.size = (400, 600)

class WelcomeScreen(Screen):
    pass

from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout

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
        top3_colors = [(1, 0.84, 0, 1),(0.75, 0.75, 0.75, 1), (0.8, 0.5, 0.2, 1)]
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




class HomepageScreen(Screen):
    def nav_draw(self, *args):
        print("Navigation button pressed!")


class RegisterScreen(Screen):
    def register(self):
        full_name = self.ids.full_name.text
        nickname = self.ids.nickname.text
        email = self.ids.email.text
        role = self.ids.role.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text

        if not full_name or not nickname or not email or not role or not password:
            print("All fields are required!")
            return

        if password != confirm_password:
            print("Passwords do not match!")
            return

        conn = sqlite3.connect("Gogreen.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (full_name, nickname, email, role, password) VALUES (?, ?, ?, ?, ?)",
                           (full_name, nickname, email, role, password))
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

class ChallengesScreen(Screen):
    pass

class MapScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class GoGreenApp(MDApp):
    def build(self):
        current_user_nickname = None

        # Initialize the app first
        self.theme_cls.primary_palette = "Green"  # You can change the theme if needed

        # Load the KV file after app initialization
        Builder.load_file("screens/welcome_screen.kv")  # welcome .kv file
        Builder.load_file("screens/reg_screen.kv")  # registration .kv file
        Builder.load_file("screens/login_screen.kv")  # login .kv file
        Builder.load_file("screens/home_screen.kv")  # home .kv file
        Builder.load_file("screens/leaderboard_screen.kv")
        Builder.load_file("screens/challenges_screen.kv")

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
