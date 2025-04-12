import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager


# Set the window size
Window.size = (400, 600)

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT, 
                    nickname TEXT UNIQUE, 
                    email TEXT UNIQUE, 
                    password TEXT)''')
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

class DashboardScreen(Screen):
    pass

class ChallengesScreen(Screen):
    pass

class VendorsScreen(Screen):
    pass

class EventsScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass



class RegisterScreen(Screen):
    def register(self):
        """Handles user registration."""
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

        # Save to database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (full_name, nickname, email, password) VALUES (?, ?, ?, ?)",
                           (full_name, nickname, email, password))
            conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Nickname or email already exists!")
        finally:
            conn.close()


class LoginScreen(Screen):
    def login(self):
        """Handles user login."""
        login_input = self.ids.login_input.text  # Can be email or nickname
        password = self.ids.password.text

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE (email=? OR nickname=?) AND password=?",
                       (login_input, login_input, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            print("Login successful!")
        else:
            print("Invalid email/nickname or password!")


class GoGreenApp(MDApp):
    def build(self):
        # Initialize the app first
        self.theme_cls.primary_palette = "Green"  # You can change the theme if needed

        # Load the KV file after app initialization
        Builder.load_file("screens/welcome_screen.kv")  # welcome .kv file
        Builder.load_file("screens/reg_screen.kv")  # registration .kv file
        Builder.load_file("screens/login_screen.kv")  # login .kv file

        # Create ScreenManager and add widgets/screens
        sm = MDScreenManager()

        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(ChallengesScreen(name="challenges"))
        sm.add_widget(VendorsScreen(name="vendors"))
        sm.add_widget(EventsScreen(name="events"))
        sm.add_widget(ProfileScreen(name="profile"))

        sm.current = "welcome"  # Start with WelcomeScreen
        return sm

if __name__ == "__main__":
    GoGreenApp().run()