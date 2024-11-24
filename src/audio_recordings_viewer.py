import os
import tkinter as tk
from tkinter import filedialog, messagebox
import simpleaudio as sa

class AudioRecordingsViewer:
    def __init__(self, parent, audio_dir='audio_recordings'):
        self.audio_dir = audio_dir
        self.window = tk.Toplevel(parent)
        self.window.title("Audio Recordings Viewer")
        self.window.geometry("600x400")
        
        # Listbox to display audio files
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(side='left', fill='y', padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.window, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side='left', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Controls Frame
        controls_frame = tk.Frame(self.window)
        controls_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.play_button = tk.Button(controls_frame, text="Play", command=self.play_audio, state=tk.DISABLED, width=10)
        self.play_button.pack(pady=10)
        
        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop_audio, state=tk.DISABLED, width=10)
        self.stop_button.pack(pady=10)
        
        self.populate_audio_files()
        self.play_obj = None
    
    def populate_audio_files(self):
        self.listbox.delete(0, tk.END)
        if not os.path.exists(self.audio_dir):
            messagebox.showerror("Error", f"Audio directory '{self.audio_dir}' does not exist.")
            return
        audio_files = sorted([f for f in os.listdir(self.audio_dir) if f.endswith('.wav')], reverse=True)
        for file in audio_files:
            self.listbox.insert(tk.END, file)
    
    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)
    
    def play_audio(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            audio_file = self.listbox.get(index)
            filepath = os.path.join(self.audio_dir, audio_file)
            try:
                wave_obj = sa.WaveObject.from_wave_file(filepath)
                self.play_obj = wave_obj.play()
                self.stop_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play audio file.\n{e}")
    
    def stop_audio(self):
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            self.stop_button.config(state=tk.DISABLED)