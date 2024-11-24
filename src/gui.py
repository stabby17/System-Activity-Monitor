import os
import tkinter as tk
from tkinter import messagebox
import threading
from system_monitor import SystemMonitor
from screenshots_viewer import ScreenshotsViewer            # For screenshots
from keystrokes_log_viewer import KeystrokesLogViewer       # For keystrokes
from audio_recordings_viewer import AudioRecordingsViewer   # For audio recordings

class MonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Activity Monitor")
        self.root.geometry("650x300")  # Set window size (width x height)
        
        # Initialize SystemMonitor instance
        self.monitor = SystemMonitor()
        self.monitor_thread = None

        # Screenshot Interval Input
        interval_frame = tk.Frame(root)
        interval_frame.pack(pady=10)
        
        # Label and Entry for screenshot interval
        tk.Label(interval_frame, text="Screenshot Interval (seconds):").pack(side='left', padx=5)
        self.interval_entry = tk.Entry(interval_frame, width=5)
        self.interval_entry.insert(0, "5")
        self.interval_entry.pack(side='left')

        # Monitoring Options
        options_frame = tk.Frame(root)
        options_frame.pack(pady=10)
        self.keylogger_var = tk.BooleanVar(value=True)
        self.screenshot_var = tk.BooleanVar(value=True)
        self.audio_var = tk.BooleanVar(value=False)
        self.keylogger_checkbox = tk.Checkbutton(options_frame, text="Enable Keylogger", variable=self.keylogger_var)
        self.keylogger_checkbox.pack(anchor='w')
        self.screenshot_checkbox = tk.Checkbutton(options_frame, text="Enable Screenshots", variable=self.screenshot_var)
        self.screenshot_checkbox.pack(anchor='w')
        self.audio_checkbox = tk.Checkbutton(options_frame, text="Enable Audio Recording", variable=self.audio_var)
        self.audio_checkbox.pack(anchor='w')

        # Control Buttons
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)
        self.start_button = tk.Button(buttons_frame, text="Start Monitoring", command=self.start_monitoring, width=15)
        self.start_button.pack(side='left', padx=5)
        self.stop_button = tk.Button(buttons_frame, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED, width=15)
        self.stop_button.pack(side='left', padx=5)

        # Action Buttons
        action_buttons_frame = tk.Frame(root)
        action_buttons_frame.pack(pady=10)
        self.show_keystrokes_button = tk.Button(action_buttons_frame, text="Show Keystrokes", command=self.show_keystrokes, width=15)
        self.show_keystrokes_button.pack(side='left', padx=5)
        self.show_pictures_button = tk.Button(action_buttons_frame, text="Show Pictures", command=self.open_screenshots_viewer, width=15)
        self.show_pictures_button.pack(side='left', padx=5)
        self.show_audio_button = tk.Button(action_buttons_frame, text="Show Recordings", command=self.show_audio_recordings, width=15)
        self.show_audio_button.pack(side='left', padx=5)

    def start_monitoring(self):
        try:
            interval = int(self.interval_entry.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the interval.")
            return
        
        enable_keylogger = self.keylogger_var.get()
        enable_screenshots = self.screenshot_var.get()
        enable_audio = self.audio_var.get()  # Retrieve audio recording state
        
        self.monitor_thread = threading.Thread(
            target=self.monitor.start_monitoring, 
            args=(interval, enable_keylogger, enable_screenshots, enable_audio),  # Pass audio recording state
            daemon=True
        )
        self.monitor_thread.start()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        # Viewer buttons remain enabled
        self.show_pictures_button.config(state=tk.NORMAL)
        self.show_keystrokes_button.config(state=tk.NORMAL)
        if enable_audio:
            self.show_audio_button.config(state=tk.NORMAL)
        
        if enable_audio:
            messagebox.showinfo("Monitoring", "System activity monitoring and audio recording started.")
        else:
            messagebox.showinfo("Monitoring", "System activity monitoring started.")

    def stop_monitoring(self):
        self.monitor.stop_monitoring()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        # Viewer buttons remain enabled
        self.show_keystrokes_button.config(state=tk.NORMAL)
        self.show_pictures_button.config(state=tk.NORMAL)
        self.show_audio_button.config(state=tk.NORMAL)
        
        messagebox.showinfo("Monitoring", "System activity monitoring stopped.")

    def show_keystrokes(self):
        KeystrokesLogViewer(self.root)

    def open_screenshots_viewer(self):
        ScreenshotsViewer(self.root, self.monitor.screenshot_dir)
    
    def show_audio_recordings(self):
        AudioRecordingsViewer(self.root, self.monitor.audio_dir)