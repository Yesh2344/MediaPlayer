import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pygame
import os
import json
import random
from mutagen.mp3 import MP3
import datetime
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

# Set customtkinter appearance and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MusicPlayer:
    def __init__(self):
        self.root = ctk.CTk()  # Using customtkinter main window
        self.root.title("Sonic Wave Music Player")
        self.root.geometry("1200x800")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Setup variables
        self.current_song = None
        self.paused = False
        self.songs = []
        self.current_index = 0
        self.is_shuffled = False
        self.repeat_mode = 'none'  # none, one, all
        
        # Load saved playlists and settings
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
        # Start visualization update
        self.update_visualization()

    def setup_ui(self):
        # Main container frame
        self.main_container = ctk.CTkFrame(self.root, fg_color="#121212")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, width=250, fg_color="#282828")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        self.create_sidebar()
        
        # Right content area
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#1e1e1e")
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
        self.create_main_content()
        
        # Bottom controls area
        self.controls_area = ctk.CTkFrame(self.root, height=150, fg_color="#282828")
        self.controls_area.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0,10))
        self.create_player_controls()

    def create_sidebar(self):
        # App Title
        title_label = ctk.CTkLabel(self.sidebar, text="Sonic Wave", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 30))
        
        # Navigation buttons
        nav_buttons = [
            ("Library", self.show_library),
            ("Playlists", self.show_playlists),
            ("Favorites", self.show_favorites),
            ("Settings", self.show_settings)
        ]
        for text, command in nav_buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, width=200)
            btn.pack(pady=5, padx=20)
        
        # Playlist section header
        playlist_label = ctk.CTkLabel(self.sidebar, text="Playlists", font=ctk.CTkFont(size=18))
        playlist_label.pack(pady=(30, 10))
        
        # Playlist listbox inside a frame for a better look
        playlist_frame = ctk.CTkFrame(self.sidebar, fg_color="#1e1e1e", width=220, height=200)
        playlist_frame.pack(pady=(0, 10), padx=10)
        playlist_frame.pack_propagate(False)
        
        self.playlist_listbox = tk.Listbox(playlist_frame, bg="#282828", fg="#ffffff", bd=0, highlightthickness=0)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # New playlist button
        new_playlist_btn = ctk.CTkButton(self.sidebar, text="New Playlist", command=self.create_playlist, width=200)
        new_playlist_btn.pack(pady=5, padx=20)

    def create_main_content(self):
        # Search area at top
        search_frame = ctk.CTkFrame(self.content_area, fg_color="#1e1e1e")
        search_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_songs)
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search songs...", height=35)
        self.search_entry.pack(fill=tk.X, padx=10, pady=10)
        
        # Song list treeview within a frame with a scrollbar
        tree_frame = ctk.CTkFrame(self.content_area, fg_color="#1e1e1e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))
        
        self.song_tree = tk.ttk.Treeview(tree_frame, columns=('Title', 'Artist', 'Duration'), show='headings')
        self.song_tree.heading('Title', text='Title')
        self.song_tree.heading('Artist', text='Artist')
        self.song_tree.heading('Duration', text='Duration')
        self.song_tree.column('Title', anchor=tk.W, width=300)
        self.song_tree.column('Artist', anchor=tk.W, width=200)
        self.song_tree.column('Duration', anchor=tk.CENTER, width=100)
        self.song_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.ttk.Scrollbar(tree_frame, orient="vertical", command=self.song_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.song_tree.configure(yscroll=scrollbar.set)
        
        # Bind double-click to play song
        self.song_tree.bind('<Double-1>', self.play_selected_song)

    def create_player_controls(self):
        # Upper controls: song info and progress
        info_frame = ctk.CTkFrame(self.controls_area, fg_color="#282828")
        info_frame.pack(fill=tk.X, padx=20, pady=(10,5))
        
        self.song_title_label = ctk.CTkLabel(info_frame, text="No song playing", font=ctk.CTkFont(size=18, weight="bold"))
        self.song_title_label.pack()
        
        self.artist_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=14))
        self.artist_label.pack()
        
        # Progress slider
        self.progress_var = tk.DoubleVar()
        self.progress_slider = ctk.CTkSlider(self.controls_area, from_=0, to=100, variable=self.progress_var, command=self.seek, width=800)
        self.progress_slider.pack(padx=20, pady=10)
        
        # Control buttons frame
        btn_frame = ctk.CTkFrame(self.controls_area, fg_color="#282828")
        btn_frame.pack(pady=10)
        
        btn_width = 60
        self.prev_btn = ctk.CTkButton(btn_frame, text="⏮", command=self.previous_song, width=btn_width, height=btn_width, corner_radius=10)
        self.prev_btn.grid(row=0, column=0, padx=10)
        
        self.play_btn = ctk.CTkButton(btn_frame, text="⏯", command=self.toggle_play, width=btn_width, height=btn_width, corner_radius=10)
        self.play_btn.grid(row=0, column=1, padx=10)
        
        self.next_btn = ctk.CTkButton(btn_frame, text="⏭", command=self.next_song, width=btn_width, height=btn_width, corner_radius=10)
        self.next_btn.grid(row=0, column=2, padx=10)
        
        self.shuffle_btn = ctk.CTkButton(btn_frame, text="🔀", command=self.toggle_shuffle, width=btn_width, height=btn_width, corner_radius=10)
        self.shuffle_btn.grid(row=0, column=3, padx=10)
        
        self.repeat_btn = ctk.CTkButton(btn_frame, text="🔁", command=self.toggle_repeat, width=btn_width, height=btn_width, corner_radius=10)
        self.repeat_btn.grid(row=0, column=4, padx=10)
        
        # Volume slider on the right side
        volume_frame = ctk.CTkFrame(self.controls_area, fg_color="#282828")
        volume_frame.pack(pady=10)
        volume_label = ctk.CTkLabel(volume_frame, text="Volume", font=ctk.CTkFont(size=14))
        volume_label.pack(side=tk.LEFT, padx=(10, 5))
        self.volume_var = tk.DoubleVar(value=70)
        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, variable=self.volume_var, command=self.set_volume, width=200)
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        
        # Visualization canvas using matplotlib embedded in a frame
        viz_frame = ctk.CTkFrame(self.controls_area, fg_color="#282828", height=150)
        viz_frame.pack(fill=tk.X, padx=20, pady=(5, 10))
        viz_frame.pack_propagate(False)
        self.fig = Figure(figsize=(8, 2), facecolor="#282828")
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        try:
            with open('music_player_data.json', 'r') as f:
                data = json.load(f)
                self.playlists = data.get('playlists', {})
                self.favorites = data.get('favorites', [])
                self.last_directory = data.get('last_directory', '')
        except FileNotFoundError:
            self.playlists = {}
            self.favorites = []
            self.last_directory = ''

    def save_data(self):
        data = {
            'playlists': self.playlists,
            'favorites': self.favorites,
            'last_directory': self.last_directory
        }
        with open('music_player_data.json', 'w') as f:
            json.dump(data, f)

    def play_selected_song(self, event=None):
        selection = self.song_tree.selection()
        if not selection:
            return
        # Use the item ID (iid) which is set as the song path
        song_path = selection[0]
        self.current_index = self.songs.index(song_path) if song_path in self.songs else 0
        self.play_song(song_path)

    def toggle_play(self):
        if self.current_song:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.paused = True

    def play_song(self, song_path):
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.current_song = song_path
            self.paused = False
            self.update_song_info()
        except pygame.error as e:
            messagebox.showerror("Error", f"Could not play song: {str(e)}")

    def update_song_info(self):
        if self.current_song:
            try:
                audio = MP3(self.current_song)
                duration = audio.info.length
                title = os.path.basename(self.current_song)
                self.song_title_label.configure(text=title)
                self.progress_slider.configure(from_=0, to=duration)
                
                # Update metadata if available
                if hasattr(audio, 'tags'):
                    if 'TIT2' in audio.tags:
                        self.song_title_label.configure(text=audio.tags['TIT2'].text[0])
                    if 'TPE1' in audio.tags:
                        self.artist_label.configure(text=audio.tags['TPE1'].text[0])
            except Exception:
                self.song_title_label.configure(text=os.path.basename(self.current_song))
                self.artist_label.configure(text="Unknown Artist")

    def update_visualization(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            try:
                # For demonstration purposes, we generate random data
                array = np.random.rand(100)
                self.ax.clear()
                self.ax.plot(array, color="#1db954")
                self.ax.set_axis_off()
                self.canvas.draw()
            except Exception:
                pass
        self.root.after(100, self.update_visualization)

    def seek(self, value):
        if self.current_song:
            pygame.mixer.music.set_pos(float(value))

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value) / 100)

    def toggle_shuffle(self):
        self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            random.shuffle(self.songs)
        else:
            self.songs.sort()

    def toggle_repeat(self):
        if self.repeat_mode == 'none':
            self.repeat_mode = 'one'
        elif self.repeat_mode == 'one':
            self.repeat_mode = 'all'
        else:
            self.repeat_mode = 'none'

    def create_playlist(self):
        name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if name:
            self.playlists[name] = []
            self.update_playlist_list()
            self.save_data()

    def update_playlist_list(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_listbox.insert(tk.END, playlist)

    def search_songs(self, *args):
        search_term = self.search_var.get().lower()
        if search_term == "search songs...":
            return
        for item in self.song_tree.get_children():
            values = self.song_tree.item(item)['values']
            title = values[0].lower() if values else ""
            if search_term in title:
                self.song_tree.selection_add(item)
            else:
                self.song_tree.selection_remove(item)

    def show_library(self):
        directory = filedialog.askdirectory(initialdir=self.last_directory)
        if directory:
            self.last_directory = directory
            self.load_songs(directory)
            self.save_data()

    def load_songs(self, directory):
        self.songs = []
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.mp3', '.wav')):
                    full_path = os.path.join(root_dir, file)
                    self.songs.append(full_path)
        self.update_song_list()

    def update_song_list(self):
        # Clear existing items
        for item in self.song_tree.get_children():
            self.song_tree.delete(item)
            
        for song in self.songs:
            try:
                audio = MP3(song)
                duration = str(datetime.timedelta(seconds=int(audio.info.length)))
                title = os.path.basename(song)
                artist = "Unknown Artist"
                
                if hasattr(audio, 'tags'):
                    if 'TIT2' in audio.tags:
                        title = audio.tags['TIT2'].text[0]
                    if 'TPE1' in audio.tags:
                        artist = audio.tags['TPE1'].text[0]
                        
                # Use the song path as the iid so it can be retrieved later
                self.song_tree.insert('', 'end', iid=song, values=(title, artist, duration))
            except Exception:
                self.song_tree.insert('', 'end', iid=song, values=(os.path.basename(song),
                                                                    "Unknown Artist",
                                                                    "Unknown"))

    def previous_song(self):
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)
            self.play_song(self.songs[self.current_index])

    def next_song(self):
        if self.songs:
            if self.repeat_mode == 'one':
                self.play_song(self.songs[self.current_index])
            else:
                self.current_index = (self.current_index + 1) % len(self.songs)
                self.play_song(self.songs[self.current_index])

    def show_playlists(self):
        messagebox.showinfo("Playlists", "Playlists functionality not yet implemented.")

    def show_favorites(self):
        messagebox.showinfo("Favorites", "Favorites functionality not yet implemented.")

    def show_settings(self):
        messagebox.showinfo("Settings", "Settings functionality not yet implemented.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
