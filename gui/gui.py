# import tkinter as tk
# from tkinter import ttk, messagebox
# from backend.downloader import VideoDownloader
# from backend.threading_manager import ThreadingManager

# class VideoDownloaderGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Video Downloader")
#         self.root.geometry("600x400")

#         # Initialize backend components
#         self.downloader = VideoDownloader()
#         self.thread_manager = ThreadingManager()

#         # Store download sessions
#         self.download_sessions = []

#         # Create main frame
#         self.main_frame = ttk.Frame(self.root, padding="10")
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         # Add the first download session block
#         self.add_download_block()

#     def add_download_block(self):
#         """Adds a new download block to the GUI."""
#         session_frame = ttk.Frame(self.main_frame, padding="5", relief=tk.GROOVE)
#         session_frame.pack(fill=tk.X, pady=5)

#         # URL input
#         ttk.Label(session_frame, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
#         url_entry = ttk.Entry(session_frame, width=40)
#         url_entry.grid(row=0, column=1, padx=5, pady=5)

#         # Start and End Time inputs
#         ttk.Label(session_frame, text="Start Time (sec):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
#         start_time_entry = ttk.Entry(session_frame, width=10)
#         start_time_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

#         ttk.Label(session_frame, text="End Time (sec):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
#         end_time_entry = ttk.Entry(session_frame, width=10)
#         end_time_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

#         # Download Button
#         download_button = ttk.Button(session_frame, text="Download", command=lambda: self.start_download(url_entry, start_time_entry, end_time_entry))
#         download_button.grid(row=2, column=0, columnspan=4, pady=10)

#         # Progress Label
#         progress_label = ttk.Label(session_frame, text="Progress: 0%", anchor=tk.W)
#         progress_label.grid(row=3, column=0, columnspan=4, pady=5, sticky=tk.W)
#         progress_label.grid_remove()  # Hide initially

#         # Add and Cancel Buttons
#         button_frame = ttk.Frame(session_frame)
#         button_frame.grid(row=4, column=0, columnspan=4, pady=5, sticky=tk.E)

#         add_button = ttk.Button(button_frame, text="Add", command=self.add_download_block)
#         add_button.pack(side=tk.RIGHT, padx=5)

#         cancel_button = ttk.Button(button_frame, text="Cancel", command=lambda: self.remove_download_block(session_frame))
#         cancel_button.pack(side=tk.RIGHT, padx=5)

#         # Store session components
#         self.download_sessions.append({
#             "frame": session_frame,
#             "url_entry": url_entry,
#             "start_time_entry": start_time_entry,
#             "end_time_entry": end_time_entry,
#             "progress_label": progress_label,
#             "add_button": add_button
#         })

#         # Ensure only the last block has the Add button visible
#         self.update_add_button_visibility()

#     def remove_download_block(self, frame):
#         """Removes a download block from the GUI."""
#         for session in self.download_sessions:
#             if session["frame"] == frame:
#                 session["frame"].destroy()
#                 self.download_sessions.remove(session)
#                 break
#         self.update_add_button_visibility()

#     def update_add_button_visibility(self):
#         """Ensures only the last download block has the Add button visible."""
#         for session in self.download_sessions:
#             session["add_button"].pack_forget()
#         if self.download_sessions:
#             self.download_sessions[-1]["add_button"].pack(side=tk.RIGHT, padx=5)

#     def start_download(self, url_entry, start_time_entry, end_time_entry):
#         """Starts a video download in a new thread."""
#         url = url_entry.get()
#         start_time = start_time_entry.get()
#         end_time = end_time_entry.get()

#         try:
#             start_time = int(start_time) if start_time else 0
#             end_time = int(end_time) if end_time else None
#         except ValueError:
#             messagebox.showerror("Error", "Start time and end time must be integers.")
#             return

#         if not url:
#             messagebox.showerror("Error", "YouTube URL cannot be empty.")
#             return

#         # Update progress label visibility
#         for session in self.download_sessions:
#             if session["url_entry"] == url_entry:
#                 session["progress_label"].grid()

#         # Add download task to the threading manager
#         self.thread_manager.add_task(self.download_task, args=(url, start_time, end_time, url_entry))
#         self.thread_manager.start_downloads()
        
#     def download_task(self, url, start_time, end_time, url_entry):
#         """Handles the video download and updates progress in the GUI."""
#         try:
#             # Progress callback function
#             def update_progress(progress):
#                 for session in self.download_sessions:
#                     if session["url_entry"] == url_entry:
#                         if progress == -1:  # Handle error progress
#                             session["progress_label"].config(text="Error during download!")
#                         else:
#                             session["progress_label"].config(text=f"Progress: {progress:.2f}%")
#                             #session["progress_bar"].set(progress)  # Assuming a progress bar exists


#             # Call the downloader with progress updates
#             path = self.downloader.download_video(url, start_time, end_time, update_progress)

#             # Update the label once the download is complete
#             for session in self.download_sessions:
#                 if session["url_entry"] == url_entry:
#                     session["progress_label"].config(text="Download complete: " + path)
                
#         except Exception as e:
#             messagebox.showerror("Download Error", str(e))


 
    
#     def update_progress(self, progress):
#         if progress == -1:
#             self.progress_label.setText("Error during download!")
#         else:
#             #self.progress_bar.setValue(progress)
#             self.progress_label.setText(f"Progress: {progress:.2f}%")


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VideoDownloaderGUI(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta
from tkinter import ttk, messagebox
from backend.downloader import VideoDownloader
from backend.threading_manager import ThreadingManager


class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("800x600")  # Increased window size

        # Initialize backend components
        self.downloader = VideoDownloader()
        self.thread_manager = ThreadingManager()

        # Store download sessions
        self.download_sessions = []

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Add the first download session block
        self.add_download_block()

    def add_download_block(self):
        """Adds a new download block to the GUI."""
        session_frame = ttk.Frame(self.main_frame, padding="5", relief=tk.GROOVE)
        session_frame.pack(fill=tk.X, pady=5)

        # URL input
        ttk.Label(session_frame, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        url_entry = ttk.Entry(session_frame, width=40)
        url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Start and End Time inputs (modified for HH:MM:SS format)
        ttk.Label(session_frame, text="Start Time (HH:MM:SS):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        start_time_entry = ttk.Entry(session_frame, width=10)
        start_time_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(session_frame, text="End Time (HH:MM:SS):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        end_time_entry = ttk.Entry(session_frame, width=10)
        end_time_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Download Button
        download_button = ttk.Button(session_frame, text="Download", command=lambda: self.start_download(url_entry, start_time_entry, end_time_entry))
        download_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Progress Label
        progress_label = ttk.Label(session_frame, text="Progress: 0%", anchor=tk.W)
        progress_label.grid(row=3, column=0, columnspan=4, pady=5, sticky=tk.W)
        progress_label.grid_remove()  # Hide initially

        # Add and Cancel Buttons
        button_frame = ttk.Frame(session_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=5, sticky=tk.E)

        add_button = ttk.Button(button_frame, text="Add", command=self.add_download_block)
        add_button.pack(side=tk.RIGHT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=lambda: self.remove_download_block(session_frame))
        cancel_button.pack(side=tk.RIGHT, padx=5)

        # Store session components
        self.download_sessions.append({
            "frame": session_frame,
            "url_entry": url_entry,
            "start_time_entry": start_time_entry,
            "end_time_entry": end_time_entry,
            "progress_label": progress_label,
            "add_button": add_button
        })

        # Ensure only the last block has the Add button visible
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

        # Update progress label visibility
        for session in self.download_sessions:
            if session["url_entry"] == url_entry:
                session["progress_label"].grid()

        # Add download task to the threading manager
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
            # Progress callback function
            def update_progress(progress):
                for session in self.download_sessions:
                    if session["url_entry"] == url_entry:
                        if progress == -1:  # Handle error progress
                            session["progress_label"].config(text="Error during download!")
                        else:
                            session["progress_label"].config(text=f"Progress: {progress:.2f}%")
                            #session["progress_bar"].set(progress)  # Assuming a progress bar exists

            # Call the downloader with progress updates
            path = self.downloader.download_video(url, start_time, end_time, update_progress)

            # Update the label once the download is complete
            for session in self.download_sessions:
                if session["url_entry"] == url_entry:
                    session["progress_label"].config(text="Download complete: " + path)
                
        except Exception as e:
            messagebox.showerror("Download Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()

