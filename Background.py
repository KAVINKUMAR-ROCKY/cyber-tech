from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
import time
import datetime
from plyer import brightness
from threading import Thread

# Kivy UI with Custom Theme
KV = """
MDScreen:
    md_bg_color: app.theme_cls.primary_dark  # Background color (Dark Mode)
    
    MDLabel:
        id: brightness_label
        text: "Brightness Level: 100%"
        halign: "center"
        font_style: "H6"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint: {"center_y": 0.7}

    MDRaisedButton:
        text: "Start Auto Brightness"
        md_bg_color: app.theme_cls.accent_color  # Muted Teal Blue
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.start_service()

    MDRaisedButton:
        text: "Stop Auto Brightness"
        md_bg_color: app.theme_cls.error_color  # Warm Peach
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: app.stop_service()
"""

# Background Service for Auto Brightness Control
class BrightnessService(Thread):
    def __init__(self, update_ui_callback):
        super().__init__()
        self.running = True
        self.start_time = time.time()
        self.update_ui_callback = update_ui_callback

    def run(self):
        while self.running:
            brightness_level = self.adjust_brightness()
            self.update_ui_callback(f"Brightness Level: {int(brightness_level * 100)}%")
            time.sleep(60)  # Check brightness every 60 seconds

    def stop(self):
        self.running = False

    def adjust_brightness(self):
        current_hour = datetime.datetime.now().hour
        screen_time = (time.time() - self.start_time) / 3600  # Convert seconds to hours

        # Default brightness levels
        if 20 <= current_hour or current_hour < 6:
            brightness_level = 0.5  # Night (50%)
        elif 6 <= current_hour < 12:
            brightness_level = 0.8  # Morning (80%)
        else:
            brightness_level = 1.0  # Daytime (100%)

        # Reduce brightness based on screen time
        if screen_time > 1:
            brightness_level = max(brightness_level - 0.3, 0.4)
        if screen_time > 2:
            brightness_level = max(brightness_level - 0.5, 0.3)

        # Apply brightness level
        brightness.set_brightness(int(brightness_level * 255))
        return brightness_level

# Main App with Custom Theme
class BrightnessApp(MDApp):
    def build(self):
        # Set Theme Colors
        self.theme_cls.primary_palette = "Teal"  # Muted Teal Blue (#80CED7)
        self.theme_cls.primary_hue = "400"
        self.theme_cls.accent_palette = "LightBlue"  # Pastel Blue (#A8DADC)
        self.theme_cls.accent_hue = "A100"
        self.theme_cls.error_palette = "DeepOrange"  # Warm Peach (#FFA07A)
        self.theme_cls.error_hue = "500"
        self.theme_cls.primary_light = (208/255, 230/255, 165/255, 1)  # Soft Sage Green (#D0E6A5)
        self.theme_cls.primary_dark = (30/255, 30/255, 30/255, 1)  # Deep Charcoal Grey (#2E2E2E)
        self.screen = Builder.load_string(KV)
        return self.screen

    def start_service(self):
        self.service = BrightnessService(self.update_label)
        self.service.start()

    def stop_service(self):
        if hasattr(self, 'service'):
            self.service.stop()
    
    def update_label(self, text):
        self.screen.ids.brightness_label.text = text

# Run the app
if __name__ == "__main__":
    BrightnessApp().run()

