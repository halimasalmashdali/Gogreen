import sqlite3
from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

# Set window size
Window.size = (400, 600)

# === DATABASE SETUP ===
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT, 
                    nickname TEXT UNIQUE, 
                    email TEXT UNIQUE, 
                    password TEXT)''')

# Challenges table
cursor.execute('''CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')

# Points table (many-to-many with extra "points" attribute)
cursor.execute('''CREATE TABLE IF NOT EXISTS points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    challenge_id INTEGER,
                    points INTEGER DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(challenge_id) REFERENCES challenges(id))''')

conn.commit()
conn.close()


# === SCREEN CLASSES ===

class WelcomeScreen(Screen):
    pass

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

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (full_name, nickname, email, password) VALUES (?, ?, ?, ?)",
                           (full_name, nickname, email, password))
            conn.commit()
            print("User registered successfully!")
            self.manager.current = "homepage"
        except sqlite3.IntegrityError:
            print("Nickname or email already exists!")
        finally:
            conn.close()


class LoginScreen(Screen):
    def login(self):
        login_input = self.ids.login_input.text
        password = self.ids.password.text

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE (email=? OR nickname=?) AND password=?",
                       (login_input, login_input, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            print("Login successful!")
            App.get_running_app().current_user_id = user[0]
            self.manager.current = "homepage"
        else:
            print("Invalid email/nickname or password!")


class HomepageScreen(Screen):
    def home_page(self):
        self.manager.current = "homepage"

    def challenges_page(self):
        self.manager.current = "challenges"

    def leaderboard_page(self):
        self.manager.current = "leaderboard"

    def map_page(self):
        self.manager.current = "map"

    def profile_page(self):
        self.manager.current = "profile"


class LeaderboardScreen(Screen):
    leaderboard_data = ListProperty([])

    def home_page(self):
        self.manager.current = "homepage"

    def challenges_page(self):
        self.manager.current = "challenges"

    def leaderboard_page(self):
        self.manager.current = "leaderboard"

    def map_page(self):
        self.manager.current = "map"

    def profile_page(self):
        self.manager.current = "profile"




    def on_enter(self):
        self.load_leaderboard()

    def load_leaderboard(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Total points per user
        cursor.execute("""
            SELECT users.nickname, SUM(points.points) as total_points, users.id
            FROM users
            JOIN points ON users.id = points.user_id
            GROUP BY users.id
            ORDER BY total_points DESC
            LIMIT 20
        """)
        all_data = cursor.fetchall()

        current_user_id = App.get_running_app().current_user_id
        top_data = []
        current_user_entry = None

        for idx, (nickname, pts, uid) in enumerate(all_data):
            place = idx + 1
            entry = (place, nickname, pts)
            if place <= 8:
                top_data.append(entry)
            if uid == current_user_id:
                current_user_entry = entry

        # If current user not in top, get their rank
        if not current_user_entry:
            cursor.execute("""
                SELECT nickname, SUM(points) as total_points
                FROM users
                JOIN points ON users.id = points.user_id
                GROUP BY users.id
                ORDER BY total_points DESC
            """)
            all_users = cursor.fetchall()
            for idx, (nickname, pts) in enumerate(all_users):
                cursor.execute("SELECT id FROM users WHERE nickname = ?", (nickname,))
                uid = cursor.fetchone()[0]
                if uid == current_user_id:
                    current_user_entry = (idx + 1, nickname, pts)
                    break

        if current_user_entry and current_user_entry not in top_data:
            top_data.append(('—', '...', '...'))  # Spacer
            top_data.append(current_user_entry)

        self.leaderboard_data = top_data
        conn.close()


# === MAIN APP ===

class GoGreenApp(MDApp):
    current_user_id = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        Builder.load_file("screens/welcome_screen.kv")
        Builder.load_file("screens/reg_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/home_screen.kv")
        Builder.load_file("screens/leaderboard_screen.kv")

        sm = MDScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomepageScreen(name="homepage"))
        sm.add_widget(LeaderboardScreen(name="leaderboard"))

        sm.current = "welcome"
        return sm


if __name__ == "__main__":
    GoGreenApp().run()
