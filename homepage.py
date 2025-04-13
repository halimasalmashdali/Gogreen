from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp

Window.size = (300, 500)

screen_helper = """
Screen:
    BoxLayout:
        orientation: 'vertical'
        spacing: 0
        
        # Main content (takes available space)
        MDBoxLayout:
            Button:
                text: "challenge"
                size_hint_y: 0.7
            Button:
                text: "challenge"
                size_hint_y: 0.7
            Button:
                text: "challenge"
                size_hint_y: 0.7

        Widget:  # Spacer
            size_hint_y: 0.5

        MDBoxLayout:
            orientation: "vertical"
            Button:
                text: "news"
                size_hint_y: 0.4
            Button:
                text: "news"
                size_hint_y: 0.4
            Button:
                text: "news"
                size_hint_y: 0.4


        # Custom bottom bar - NO FAB SPACE
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: app.theme_cls.primary_color
            padding: dp(10)
            
            MDIconButton:
                icon: "home"
                on_release: app.nav_draw()
                theme_text_color: "Custom"
                text_color: "white"

            Widget:  # Spacer
                size_hint_x: 0.5

            MDIconButton:
                icon: "check-circle"
                on_release: app.nav_draw()
                theme_text_color: "Custom"
                text_color: "white"

            Widget:  # Spacer
                size_hint_x: 0.5

            MDIconButton:
                icon: "trophy"
                on_release: app.nav_draw()
                theme_text_color: "Custom"
                text_color: "white"
            
            Widget:  # Spacer
                size_hint_x: 0.5
  
            MDIconButton:
                icon: "map"
                on_release: app.nav_draw()
                theme_text_color: "Custom"
                text_color: "white"


            Widget:  # Spacer
                size_hint_x: 0.5

            MDIconButton:
                icon: "account"
                on_release: app.nav_draw()
                theme_text_color: "Custom"
                text_color: "white"

"""

class GoGreenApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(screen_helper)
    
    def nav_draw(self, *args):
        print("Navigation button pressed!")

GoGreenApp().run()