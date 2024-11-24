import os
import tkinter as tk
from tkinter import filedialog, messagebox

class KeystrokesLogViewer:
    def __init__(self, parent, log_dir='logs'):
        self.log_dir = log_dir
        self.window = tk.Toplevel(parent)
        self.window.title("Keystrokes Log Viewer")
        self.window.geometry("600x400")

        # Listbox to display log files
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(side='left', fill='y', padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.display_log)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.window, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side='left', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Text widget to display log content
        self.text = tk.Text(self.window, wrap='word')
        self.text.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        self.text.config(state='disabled')

        self.populate_log_files()

    def populate_log_files(self):
        self.listbox.delete(0, tk.END)
        if not os.path.exists(self.log_dir):
            messagebox.showerror("Error", f"Log directory '{self.log_dir}' does not exist.")
            return
        log_files = sorted([f for f in os.listdir(self.log_dir) if f.endswith('.txt')], reverse=True)
        for file in log_files:
            self.listbox.insert(tk.END, file)

    def display_log(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            log_file = event.widget.get(index)
            filepath = os.path.join(self.log_dir, log_file)
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                self.text.config(state='normal')
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, content)
                self.text.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open log file.\n{e}")