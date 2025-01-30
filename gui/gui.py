import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta
from backend.downloader import VideoDownloader
from backend.threading_manager import ThreadingManager

class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Video Downloader")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        self.style.map("TButton", background=[("active", "#4a4a4a")])

        # Initialize backend components
        self.downloader = VideoDownloader()
        self.thread_manager = ThreadingManager()
        self.download_sessions = []

        # Create scrollable container
        self.canvas = tk.Canvas(root, bg="#f0f0f0", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

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

        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Add initial download block
        self.add_download_block()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_download_block(self):
        """Adds a new download block to the GUI."""
        # Container to center the session_frame
        container_frame = ttk.Frame(self.scrollable_frame)
        container_frame.pack(fill=tk.X, pady=5)

        # Main session frame
        session_frame = ttk.Frame(container_frame, padding=10, style="TFrame")
        session_frame.pack(anchor="center", pady=5, ipadx=10, ipady=5)

        # URL Section
        url_frame = ttk.Frame(session_frame)
        url_frame.pack(fill=tk.X, pady=5)
        ttk.Label(url_frame, text="YouTube URL:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        url_entry = ttk.Entry(url_frame, width=50, font=("Arial", 10))
        url_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Time Inputs
        time_frame = ttk.Frame(session_frame)
        time_frame.pack(fill=tk.X, pady=5)

        # Start Time with blue scheme
        start_frame = ttk.Frame(time_frame)
        start_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(start_frame, text="Start Time (HH:MM:SS):", 
                bg="#e3f2fd", fg="#1976d2", font=("Arial", 9, "bold"), 
                padx=5, pady=2).pack()
        start_time_entry = ttk.Entry(start_frame, width=15, font=("Arial", 10))
        start_time_entry.pack(pady=2)

        # End Time with pink scheme
        end_frame = ttk.Frame(time_frame)
        end_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(end_frame, text="End Time (HH:MM:SS):", 
                bg="#fce4ec", fg="#d81b60", font=("Arial", 9, "bold"), 
                padx=5, pady=2).pack()
        end_time_entry = ttk.Entry(end_frame, width=15, font=("Arial", 10))
        end_time_entry.pack(pady=2)

        # Progress Section
        progress_frame = ttk.Frame(session_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        progress_label = ttk.Label(progress_frame, text="Ready to download", font=("Arial", 9))
        progress_label.pack(side=tk.LEFT)
        
        # Button Container
        button_frame = ttk.Frame(session_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Action Buttons
        btn_style = {"style": "TButton", "width": 11}
        download_btn = ttk.Button(button_frame, text="Download", 
                                command=lambda: self.start_download(url_entry, start_time_entry, end_time_entry),
                                **btn_style)
        download_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Remove", 
                              command=lambda: self.remove_download_block(container_frame),
                              **btn_style)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

        add_btn = ttk.Button(button_frame, text="Add New", 
                           command=self.add_download_block,
                           **btn_style)
        add_btn.pack(side=tk.RIGHT, padx=5)

        # Store session components
        self.download_sessions.append({
            "frame": container_frame,
            "url_entry": url_entry,
            "start_time_entry": start_time_entry,
            "end_time_entry": end_time_entry,
            "progress_label": progress_label,
            "add_button": add_btn
        })

        self.update_add_button_visibility()

    def remove_download_block(self, frame):
        """Removes a download block from the GUI."""
        for session in self.download_sessions:
            if session["frame"] == frame:
                session["frame"].destroy()
                self.download_sessions.remove(session)
                break
        self.update_add_button_visibility()

    def update_add_button_visibility(self):
        """Ensures only the last download block has the Add button visible."""
        for session in self.download_sessions:
            session["add_button"].pack_forget()
        if self.download_sessions:
            self.download_sessions[-1]["add_button"].pack(side=tk.RIGHT, padx=5)

    def start_download(self, url_entry, start_time_entry, end_time_entry):
        """Starts a video download in a new thread."""
        url = url_entry.get()
        start_time_str = start_time_entry.get()
        end_time_str = end_time_entry.get()

        start_time = self.convert_time_to_seconds(start_time_str)
        end_time = self.convert_time_to_seconds(end_time_str) if end_time_str else None

        if start_time is None or (end_time is not None and end_time < start_time):
            messagebox.showerror("Error", "Invalid time format or end time is before start time.")
            return

        if not url:
            messagebox.showerror("Error", "YouTube URL cannot be empty.")
            return

        # Update progress label
        for session in self.download_sessions:
            if session["url_entry"] == url_entry:
                session["progress_label"].config(text="Starting download...")

        # Add download task to threading manager
        self.thread_manager.add_task(self.download_task, args=(url, start_time, end_time, url_entry))
        self.thread_manager.start_downloads()

    def convert_time_to_seconds(self, time_str):
        """Converts time in HH:MM:SS format to seconds."""
        if not time_str:
            return 0
        try:
            parts = list(map(int, time_str.split(":")))
            if len(parts) == 3:  # HH:MM:SS
                return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2]).total_seconds()
            elif len(parts) == 2:  # MM:SS
                return timedelta(minutes=parts[0], seconds=parts[1]).total_seconds()
            elif len(parts) == 1:  # SS
                return parts[0]
        except ValueError:
            return None

    def download_task(self, url, start_time, end_time, url_entry):
        """Handles the video download and updates progress in the GUI."""
        try:
            def update_progress(progress):
                for session in self.download_sessions:
                    if session["url_entry"] == url_entry:
                        if progress == -1:
                            session["progress_label"].config(text="Error during download!", foreground="red")
                        else:
                            session["progress_label"].config(
                                text=f"Downloading... {progress:.2f}%",
                                foreground="#2e7d32"
                            )

            path = self.downloader.download_video(url, start_time, end_time, update_progress)

            for session in self.download_sessions:
                if session["url_entry"] == url_entry:
                    session["progress_label"].config(
                        text=f"Download complete: {path}",
                        foreground="#2e7d32"
                    )
                
        except Exception as e:
            messagebox.showerror("Download Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()