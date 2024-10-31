import keyboard
import os
import time
from datetime import datetime
import platform
import argparse

# Try importing the appropriate screenshot module
try:
    if platform.system() == "Windows":
        from PIL import ImageGrab
    else:  # Linux/Mac
        import pyscreenshot as ImageGrab
except ImportError as e:
    print("Error: Required modules not found.")
    print("Please install: pip3 install pillow pyscreenshot")
    exit(1)

class SystemMonitor:
    def __init__(self):
        self.log_file = 'system_activity.txt'
        self.screenshot_dir = 'activity_snapshots'
        
        print("System activity monitoring has started")
        print("This tool is logging keyboard events and taking periodic screenshots")
        
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            
        with open(self.log_file, 'a') as f:
            f.write(f"\nMonitoring started at {datetime.now()}\n")

    def on_key_press(self, event):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp}: {event.name}\n")

    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            
            with open(self.log_file, 'a') as f:
                f.write(f"Screenshot saved: {filepath}\n")
        except Exception as e:
            with open(self.log_file, 'a') as f:
                f.write(f"Screenshot error: {str(e)}\n")

    def start_monitoring(self, screenshot_interval):
        keyboard.on_press(self.on_key_press)
        
        try:
            while True:
                self.take_screenshot()
                time.sleep(screenshot_interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            with open(self.log_file, 'a') as f:
                f.write(f"\nMonitoring stopped at {datetime.now()}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='System Activity Monitor')
    parser.add_argument('-i', '--interval', 
                        type=int, 
                        default=5,
                        help='Screenshot interval in seconds (default: 5)')
    
    args = parser.parse_args()
    
    print(f"Starting monitor with {args.interval} second screenshot interval")
    print("Press Ctrl+C to stop")
    time.sleep(2)
    
    monitor = SystemMonitor()
    monitor.start_monitoring(args.interval)