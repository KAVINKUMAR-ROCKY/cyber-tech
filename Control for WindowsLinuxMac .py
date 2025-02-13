# Auto Brightness Control for Windows/Linux/Mac
# Runs in the background and adjusts brightness automatically

import time
import datetime
import screen_brightness_control as sbc
from threading import Thread

# Define a background service for brightness control
class BrightnessService(Thread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        start_time = time.time()
        while self.running:
            adjust_brightness(start_time)
            time.sleep(60)  # Check brightness every 60 seconds

    def stop(self):
        self.running = False

# Function to calculate runtime
def get_runtime(start_time):
    return time.time() - start_time

# Function to adjust brightness dynamically
def adjust_brightness(start_time):
    current_hour = datetime.datetime.now().hour
    screen_time = get_runtime(start_time) / 3600  # Convert seconds to hours

    if 20 <= current_hour or current_hour < 6:  # Night time (8 PM - 6 AM)
        brightness_level = 50  # 50%
    elif 6 <= current_hour < 12:  # Morning (6 AM - 12 PM)
        brightness_level = 80  # 80%
    else:  # Daytime (12 PM - 8 PM)
        brightness_level = 100  # 100%
    
    # Reduce brightness based on screen time usage
    if screen_time > 1:  # After 1 hour
        brightness_level = max(brightness_level - 30, 40)  # Reduce but keep min 40%
    if screen_time > 2:  # After 2 hours
        brightness_level = max(brightness_level - 50, 30)  # Reduce but keep min 30%
    
    # Set screen brightness on PC
    sbc.set_brightness(brightness_level)
    print(f"Brightness set to {brightness_level}% at {datetime.datetime.now().strftime('%H:%M')} | Screen time: {screen_time:.2f} hours")

# Start the background service
if __name__ == "__main__":
    service = BrightnessService()
    service.start()
