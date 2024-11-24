import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


class ScreenshotsViewer:
    def __init__(self, parent, screenshot_dir):
        self.window = tk.Toplevel(parent)
        self.window.title("Screenshots Viewer")
        self.window.geometry("800x600")
        self.screenshot_dir = screenshot_dir
        self.image_size = (100, 100)
        self.images = []
        self.checkboxes = []

        # Buttons Frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(fill='x', pady=5)

        # Refresh Button
        self.refresh_button = tk.Button(buttons_frame, text="Refresh", command=self.load_images)
        self.refresh_button.pack(side='left', padx=5)

        # Select All Button
        self.select_all_button = tk.Button(buttons_frame, text="Select All", command=self.select_all)
        self.select_all_button.pack(side='left', padx=5)

        # Delete Selected Button (Destructive - Red)
        self.delete_button = tk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_selected,
            state=tk.DISABLED,
            bg='red',
            fg='white',
            activebackground='dark red',
            activeforeground='white'
        )
        self.delete_button.pack(side='left', padx=5)
        # Bind hover effects
        self.delete_button.bind("<Enter>", self.on_delete_hover)
        self.delete_button.bind("<Leave>", self.on_delete_leave)

        # Export Selected Button
        self.export_button = tk.Button(
            buttons_frame,
            text="Export Selected",
            command=self.export_selected,
            state=tk.DISABLED
        )
        self.export_button.pack(side='left', padx=5)

        # Exit Button
        self.exit_button = tk.Button(buttons_frame, text="Exit", command=self.window.destroy)
        self.exit_button.pack(side='right', padx=5)

        # Thumbnails Canvas with Scrollbar
        self.canvas = tk.Canvas(self.window)
        self.scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_images()

    def on_delete_hover(self, event):
        self.delete_button.config(bg='dark red')

    def on_delete_leave(self, event):
        self.delete_button.config(bg='red')

    def load_images(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.images.clear()
        self.checkboxes.clear()
        files = sorted(
            os.listdir(self.screenshot_dir),
            key=lambda x: os.path.getctime(os.path.join(self.screenshot_dir, x)),
            reverse=True
        )
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if not image_files:
            tk.Label(self.scrollable_frame, text="No screenshots available.", font=("Arial", 14)).pack(pady=20)
            self.update_action_buttons()
            return
        for idx, image_file in enumerate(image_files):
            image_path = os.path.join(self.screenshot_dir, image_file)
            try:
                img = Image.open(image_path)
                img.thumbnail(self.image_size)
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)
                frame = tk.Frame(self.scrollable_frame, bd=2, relief='groove')
                frame.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)

                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(frame, variable=var, command=self.update_action_buttons)
                checkbox.pack(anchor='nw')
                self.checkboxes.append((var, image_path))

                label = tk.Label(frame, image=photo, cursor="hand2")
                label.pack()
                label.bind("<Button-1>", lambda e, path=image_path: self.open_full_image(path))
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

        self.update_action_buttons()

    def update_action_buttons(self):
        any_selected = any(var.get() for var, _ in self.checkboxes)
        self.delete_button.config(state=tk.NORMAL if any_selected else tk.DISABLED)
        self.export_button.config(state=tk.NORMAL if any_selected else tk.DISABLED)

    def delete_selected(self):
        to_delete = [path for var, path in self.checkboxes if var.get()]
        if not to_delete:
            messagebox.showinfo("Delete Screenshots", "No screenshots selected for deletion.")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"You are about to delete {len(to_delete)} screenshot(s). This action cannot be undone.\n\nDo you wish to proceed?",
            icon='warning'
        )
        if confirm:
            for path in to_delete:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Error deleting {path}: {e}")
            self.load_images()
            messagebox.showinfo("Delete Screenshots", "Selected screenshots have been deleted.")
            # Reset Select All button if deletions affect selections
            self.select_all_button.config(state=tk.NORMAL)

    def export_selected(self):
        to_export = [path for var, path in self.checkboxes if var.get()]
        if not to_export:
            messagebox.showinfo("Export Screenshots", "No screenshots selected for export.")
            return

        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return

        for path in to_export:
            try:
                filename = os.path.basename(path)
                destination = os.path.join(export_dir, filename)
                with open(path, 'rb') as src_file:
                    with open(destination, 'wb') as dest_file:
                        dest_file.write(src_file.read())
            except Exception as e:
                print(f"Error exporting {path}: {e}")

        messagebox.showinfo("Export Screenshots", f"Exported {len(to_export)} screenshot(s) to {export_dir}.")

    def select_all(self):
        for var, _ in self.checkboxes:
            var.set(True)
        self.update_action_buttons()

    def open_full_image(self, image_path):
        full_image_window = tk.Toplevel(self.window)
        full_image_window.title(os.path.basename(image_path))
        full_image_window.geometry("800x600")

        try:
            img = Image.open(image_path)
            img_ratio = img.width / img.height
            window_width = 800
            window_height = 600
            window_ratio = window_width / window_height

            if img_ratio > window_ratio:
                new_width = window_width
                new_height = int(new_width / img_ratio)
            else:
                new_height = window_height
                new_width = int(new_height * img_ratio)

            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(full_image_window, image=photo)
            label.image = photo
            label.pack(expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image.\n{e}")