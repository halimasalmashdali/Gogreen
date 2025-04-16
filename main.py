import sqlite3
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
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

class LeaderboardScreen(Screen):
        leaderboard_data = ListProperty([])

        def on_enter(self):
            self.load_data()

        def load_data(self):
            conn = sqlite3.connect('GoGreen.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, SUM(points) FROM points GROUP BY id ORDER BY SUM(points) DESC")
            self.leaderboard_data = cursor.fetchall()
            conn.close()

class HomepageScreen(Screen):
    def nav_draw(self, *args):
        print("Navigation button pressed!")


class RegisterScreen(Screen):
    def register(self):
        full_name = self.ids.full_name.text
        nickname = self.ids.nickname.text
        email = self.ids.email.text
        role = self.ids.text
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
        # Initialize the app first
        self.theme_cls.primary_palette = "Green"  # You can change the theme if needed

        # Load the KV file after app initialization
        Builder.load_file("screens/welcome_screen.kv")  # welcome .kv file
        Builder.load_file("screens/reg_screen.kv")  # registration .kv file
        Builder.load_file("screens/login_screen.kv")  # login .kv file
        Builder.load_file("screens/home_screen.kv")  # home .kv file
        Builder.load_file("screens/leaderboard_screen.kv")

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
