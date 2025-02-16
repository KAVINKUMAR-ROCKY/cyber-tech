from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from plyer import brightness
import datetime

# Define the color scheme
COLORS = {
    "primary_sage_green": "#D0E6A5",
    "primary_teal_blue": "#80CED7",
    "primary_charcoal_grey": "#2E2E2E",
    "accent_warm_peach": "#FFA07A",
    "accent_pastel_blue": "#A8DADC",
    "bg_off_white": "#F7F7F7",
    "bg_night_blue": "#1B263B"
}

class SmartGazeZenUI(BoxLayout):
    def adjust_brightness(self):
        """Adjust screen brightness based on time of day"""
        current_hour = datetime.datetime.now().hour
        if 20 <= current_hour or current_hour < 6:  # Night time (8 PM - 6 AM)
            brightness_level = 0.5  # 50%
        elif 6 <= current_hour < 12:  # Morning (6 AM - 12 PM)
            brightness_level = 0.8  # 80%
        else:  # Daytime (12 PM - 8 PM)
            brightness_level = 1.0  # 100%

        brightness.set_brightness(int(brightness_level * 255))
        self.ids.brightness_btn.text = f"Brightness: {int(brightness_level * 100)}%"

    def toggle_dark_mode(self, instance):
        """Switch between light mode and dark mode"""
        if instance.state == "down":
            self.bg_color = COLORS["bg_night_blue"]  # Dark mode
            self.ids.title_label.color = COLORS["primary_sage_green"]
            instance.text = "Disable Dark Mode"
        else:
            self.bg_color = COLORS["bg_off_white"]  # Light mode
            self.ids.title_label.color = COLORS["primary_teal_blue"]
            instance.text = "Enable Dark Mode"

class SmartGazeZenApp(App):
    def build(self):
        return SmartGazeZenUI()

if __name__ == "__main__":
    SmartGazeZenApp().run()
