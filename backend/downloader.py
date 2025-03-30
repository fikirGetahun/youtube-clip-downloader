 



    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None):
    #     try:
    #         print(f"Starting download for URL: {url}")

    #         # Specify the location of FFmpeg
    #         ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #         # yt-dlp options for format selection
    #         ydl_opts = {
    #             "quiet": False,
    #             "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #             "noplaylist": True,
    #             "force_generic_extractor": True,
    #             "http_headers": {
    #                 "User-Agent": "Mozilla/5.0",
    #             },
    #             "ffmpeg_location": ffmpeg_path,
    #         }

    #         # Extract video info with yt-dlp
    #         with YoutubeDL(ydl_opts) as ydl:
    #             video_info = ydl.extract_info(url, download=False)

    #             video_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #                 ),
    #                 key=lambda f: (
    #                     f.get("height", 0) or 0,  # Use 0 if height is None
    #                     f.get("fps", 0) or 0      # Use 0 if fps is None
    #                 ),
    #                 default=None,
    #             )
    #             audio_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("acodec") and fmt.get("acodec") != "none"
    #                 ),
    #                 key=lambda f: f.get("abr", 0) or 0,  # Use 0 if abr is None
    #                 default=None,
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("No valid video or audio stream found.")

    #             video_url = video_stream["url"]
    #             audio_url = audio_stream["url"]

    #             # Video title and duration
    #             video_title = video_info.get("title", "downloaded_video").replace(" ", "_")
    #             total_duration = video_info["duration"]
    #             clip_duration = total_duration if end_time is None else (end_time - start_time)

    #             # FFmpeg command to clip both video and audio
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "error",
    #                 "-progress", "pipe:1",  # Output progress to stdout
    #                 "-filter_complex", "[0:a][1:v]concat=n=1:v=1:a=1",
    #                 # "-hwaccel", "nvdec",  # Enable hardware acceleration (Intel QSV)
    #                 "-i", audio_url,
    #                 "-i", video_url,
    #                 "-ss", str(start_time),  # Seek to start time for video
    #                 "-ss", str(start_time),  # Seek to start time for audio
    #                 "-c:v", "h264_nvenc",  # Video encoding using hardware acceleration (Intel QSV)
    #                 "-c:a", "aac",  # Audio encoding
    #                 "-t", str(clip_duration),  # Clip duration (from start_time to start_time + duration)
    #                 "-movflags", "+faststart",  # Ensure header is at the beginning for quicker playback
    #                 "-y",  # Overwrite the output file if it exists
    #                 os.path.join(self.download_folder, f"{video_title}_clipped.mp4"),
    #             ]

    #             print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #             # Limit CPU usage by setting affinity (e.g., limit to 1 CPU core)
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 # stderr=subprocess.STDOUT,
    #                 stderr=subprocess.PIPE,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

 

    #             # Set CPU affinity to limit CPU usage to a specific core
    #             # Limit CPU usage by setting affinity (e.g., limit to 1 CPU core)
    #             # if psutil:
    #             #     pid = process.pid
    #             #     p = psutil.Process(pid)
    #             #     p.cpu_affinity([0])  # Limiting the process to use only CPU 0 (you can adjust this)
    #             #     print(f"CPU affinity set to core 0 for process {pid}")

    #             #     # Reduce priority of the process to lower CPU usage
    #             #     p.nice(psutil.IDLE_PRIORITY_CLASS)  # Decreases priority for FFmpeg process
    #             # This limits the FFmpeg process to 50% of a single CPU core (you can adjust the limit)
                
                
    #             # Give FFmpeg process a moment to start before applying resource limits
                
    #             # Use Process Lasso to limit CPU usage to a percentage (e.g., 10%)
    #             # prlasso_cmd = [
    #             #     "C:\\Program Files\\Process Lasso\\prlasso.exe",  # Path to prlasso.exe
    #             #     "CPU",  # CPU action (to set limits)
    #             #     str(process.pid),  # The process PID of FFmpeg
    #             #     "/limit",  # Limit the CPU usage
    #             #     "10",  # 10% CPU limit (adjust as needed)
    #             # ]

    #             # Execute Process Lasso command to limit FFmpeg CPU usage
    #             # subprocess.run(prlasso_cmd, check=True)
    #             # print(f"Applied CPU limit to FFmpeg process with PID {process.pid}")
                
                
    #             # Track progress
    #             while process.poll() is None:
    #                 if process.stdout:
    #                     for line in process.stdout:
    #                         if "out_time_ms" in line:
    #                             # Parse elapsed time
    #                             time_match = re.search(r"out_time_ms=(\d+)", line)
    #                             if time_match:
    #                                 elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                                 progress = (elapsed_time / clip_duration) * 100
    #                                 if update_progress_callback:
    #                                     update_progress_callback(min(100, progress))

    #             # Ensure the process has completed before accessing the file
    #             process.wait()

    #             # Add a small delay to ensure the file is fully written to disk
    #             time.sleep(2)  # Wait for 2 seconds to ensure the file is fully written

    #             # Check for errors
    #             if process.returncode != 0:
    #                 error_output = process.stdout.read() if process.stdout else "Unknown error"
    #                 print(f"FFmpeg error: {error_output}")
    #                 if update_progress_callback:
    #                     update_progress_callback(-1)  # Indicate failure with -1
    #                 raise RuntimeError("FFmpeg failed to process the video.")

    #             # Final confirmation that download has completed
    #             video_file_path = os.path.join(self.download_folder, f"{video_title}_clipped.mp4")
    #             print(f"Download completed: {video_file_path}")
    #             if update_progress_callback:
    #                 update_progress_callback(100)  # Mark as complete
    #             return video_file_path

    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         if update_progress_callback:
    #             update_progress_callback(-1)  # Indicate failure with -1
    #         raise ValueError(f"An error occurred while downloading the video: {e}")

    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None):
        # try:
            # print(f"Starting download for URL: {url}")

            # # Specify the location of FFmpeg
            # ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

            # # yt-dlp options for format selection
            # ydl_opts = {
                # "quiet": False,
                # "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
                # "noplaylist": True,
                # "http_headers": {
                    # "User-Agent": "Mozilla/5.0",
                # },
                # "ffmpeg_location": ffmpeg_path,
            # }

            # # Extract video info with yt-dlp
            # with YoutubeDL(ydl_opts) as ydl:
                # video_info = ydl.extract_info(url, download=False)

                # video_stream = max(
                    # (
                        # fmt for fmt in video_info["formats"]
                        # if fmt.get("vcodec") and fmt.get("vcodec") != "none"
                    # ),
                    # key=lambda f: (
                        # f.get("height", 0) or 0,  # Use 0 if height is None
                        # f.get("fps", 0) or 0      # Use 0 if fps is None
                    # ),
                    # default=None,
                # )
                # audio_stream = max(
                    # (
                        # fmt for fmt in video_info["formats"]
                        # if fmt.get("acodec") and fmt.get("acodec") != "none"
                    # ),
                    # key=lambda f: f.get("abr", 0) or 0,  # Use 0 if abr is None
                    # default=None,
                # )

                # if not video_stream or not audio_stream:
                    # raise ValueError("No valid video or audio stream found.")

                # video_url = video_stream["url"]
                # audio_url = audio_stream["url"]

                # # Video title and duration
                # video_title = video_info.get("title", "downloaded_video").replace(" ", "_")
                # total_duration = video_info["duration"]
                # clip_duration = total_duration if end_time is None else (end_time - start_time)

                # # FFmpeg command to clip both video and audio
                # ffmpeg_cmd = [
                    # ffmpeg_path,
                    # "-loglevel", "error",
                    # "-progress", "pipe:1",  # Output progress to stdout
                    # "-hwaccel", "qsv",  # Enable hardware acceleration (Intel QSV)
                    # "-i", audio_url,
                    # "-i", video_url,
                    # "-ss", str(start_time),  # Seek to start time for video
                    # "-ss", str(start_time),  # Seek to start time for audio
                    # "-c:v", "h264_qsv",  # Video encoding using hardware acceleration (Intel QSV)
                    # "-c:a", "aac",  # Audio encoding
                    # "-t", str(clip_duration),  # Clip duration (from start_time to start_time + duration)
                    # "-y",  # Overwrite the output file if it exists
                    # os.path.join(self.download_folder, f"{video_title}_clipped.mp4"),
                # ]

                # print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

                # # Limit CPU usage by setting affinity (e.g., limit to 1 CPU core)
                # if psutil:
                    # process = subprocess.Popen(
                        # ffmpeg_cmd,
                        # stdout=subprocess.PIPE,
                        # stderr=subprocess.STDOUT,
                        # universal_newlines=True,
                        # bufsize=1,
                    # )
                    # # Set CPU affinity here to limit CPU usage
                    # pid = process.pid
                    # p = psutil.Process(pid)
                    # p.cpu_affinity([0])  # Limiting the process to use only CPU 0 (you can adjust this)
                    # print(f"CPU affinity set to core 0 for process {pid}")

                # # Use subprocess.Popen to capture real-time progress
                # process = subprocess.Popen(
                    # ffmpeg_cmd,
                    # stdout=subprocess.PIPE,
                    # stderr=subprocess.STDOUT,
                    # universal_newlines=True,
                    # bufsize=1,
                # )

                # # Track progress
                # while process.poll() is None:
                    # if process.stdout:
                        # for line in process.stdout:
                            # if "out_time_ms" in line:
                                # # Parse elapsed time
                                # time_match = re.search(r"out_time_ms=(\d+)", line)
                                # if time_match:
                                    # elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
                                    # progress = (elapsed_time / clip_duration) * 100
                                    # if update_progress_callback:
                                        # update_progress_callback(min(100, progress))

                # # Check for errors
                # if process.returncode != 0:
                    # error_output = process.stdout.read() if process.stdout else "Unknown error"
                    # print(f"FFmpeg error: {error_output}")
                    # if update_progress_callback:
                        # update_progress_callback(-1)  # Indicate failure with -1
                    # raise RuntimeError("FFmpeg failed to process the video.")

                # print(f"Download completed: {os.path.join(self.download_folder, f'{video_title}_clipped.mp4')}")
                # if update_progress_callback:
                    # update_progress_callback(100)  # Mark as complete
                # return os.path.join(self.download_folder, f"{video_title}_clipped.mp4")

        # except Exception as e:
            # print(f"An error occurred: {e}")
            # if update_progress_callback:
                # update_progress_callback(-1)  # Indicate failure with -1
            # raise ValueError(f"An error occurred while downloading the video: {e}")

    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None):
    #     try:
    #         print(f"Starting download for URL: {url}")

    #         # Specify the location of FFmpeg
    #         ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #         # yt-dlp options for format selection
    #         ydl_opts = {
    #             "quiet": False,
    #             "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #             "noplaylist": True,
    #             "http_headers": {
    #                 "User-Agent": "Mozilla/5.0",
    #             },
    #             "ffmpeg_location": ffmpeg_path,
    #         }

    #         # Extract video info with yt-dlp
    #         with YoutubeDL(ydl_opts) as ydl:
    #             video_info = ydl.extract_info(url, download=False)

    #             video_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #                 ),
    #                 key=lambda f: (
    #                     f.get("height", 0) or 0,  # Use 0 if height is None
    #                     f.get("fps", 0) or 0      # Use 0 if fps is None
    #                 ),
    #                 default=None,
    #             )
    #             audio_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("acodec") and fmt.get("acodec") != "none"
    #                 ),
    #                 key=lambda f: f.get("abr", 0) or 0,  # Use 0 if abr is None
    #                 default=None,
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("No valid video or audio stream found.")

    #             video_url = video_stream["url"]
    #             audio_url = audio_stream["url"]

    #             # Video title and duration
    #             video_title = video_info.get("title", "downloaded_video").replace(" ", "_")
    #             total_duration = video_info["duration"]
    #             clip_duration = total_duration if end_time is None else (end_time - start_time)

    #             # FFmpeg command to clip both video and audio
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "error",
    #                 "-progress", "pipe:1",  # Output progress to stdout
    #                 "-hwaccel", "qsv",  # Enable hardware acceleration (Intel QSV)
    #                 "-i", audio_url,
    #                 "-i", video_url,
    #                 "-ss", str(start_time),  # Seek to start time for video
    #                 "-ss", str(start_time),  # Seek to start time for audio
    #                 "-c:v", "h264_qsv",  # Video encoding using hardware acceleration (Intel QSV)
    #                 "-c:a", "aac",  # Audio encoding
    #                 "-t", str(clip_duration),  # Clip duration (from start_time to start_time + duration)
    #                 "-y",  # Overwrite the output file if it exists
    #                 os.path.join(self.download_folder, f"{video_title}_clipped.mp4"),
    #             ]

    #             print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #             # Use subprocess.Popen to capture real-time progress
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.STDOUT,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

    #             # Track progress
    #             while process.poll() is None:
    #                 if process.stdout:
    #                     for line in process.stdout:
    #                         if "out_time_ms" in line:
    #                             # Parse elapsed time
    #                             time_match = re.search(r"out_time_ms=(\d+)", line)
    #                             if time_match:
    #                                 elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                                 progress = (elapsed_time / clip_duration) * 100
    #                                 if update_progress_callback:
    #                                     update_progress_callback(min(100, progress))

    #             # Check for errors
    #             if process.returncode != 0:
    #                 error_output = process.stdout.read() if process.stdout else "Unknown error"
    #                 print(f"FFmpeg error: {error_output}")
    #                 if update_progress_callback:
    #                     update_progress_callback(-1)  # Indicate failure with -1
    #                 raise RuntimeError("FFmpeg failed to process the video.")

    #             print(f"Download completed: {os.path.join(self.download_folder, f'{video_title}_clipped.mp4')}")
    #             if update_progress_callback:
    #                 update_progress_callback(100)  # Mark as complete
    #             return os.path.join(self.download_folder, f"{video_title}_clipped.mp4")

    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         if update_progress_callback:
    #             update_progress_callback(-1)  # Indicate failure with -1
    #         raise ValueError(f"An error occurred while downloading the video: {e}")

 
 
    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None):
    #     try:
    #         print(f"Starting download for URL: {url}")

    #         # Specify the location of FFmpeg
    #         ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #         # yt-dlp options for format selection
    #         ydl_opts = {
    #             "quiet": False,
    #             "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #             "noplaylist": True,
    #             "http_headers": {
    #                 "User-Agent": "Mozilla/5.0",
    #             },
    #             "ffmpeg_location": ffmpeg_path,
    #         }

    #         # Extract video info with yt-dlp
    #         with YoutubeDL(ydl_opts) as ydl:
    #             video_info = ydl.extract_info(url, download=False)

    #         # Get video and audio stream URLs
    #         video_stream = max(
    #             (
    #                 fmt for fmt in video_info["formats"]
    #                 if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #             ),
    #             key=lambda f: (
    #                 f.get("height", 0) or 0,
    #                 f.get("fps", 0) or 0
    #             ),
    #             default=None,
    #         )
    #         audio_stream = max(
    #             (
    #                 fmt for fmt in video_info["formats"]
    #                 if fmt.get("acodec") and fmt.get("acodec") != "none"
    #             ),
    #             key=lambda f: f.get("abr", 0) or 0,
    #             default=None,
    #         )

    #         if not video_stream or not audio_stream:
    #             raise ValueError("No valid video or audio stream found.")

    #         video_url = video_stream["url"]
    #         audio_url = audio_stream["url"]

    #         # Video title and duration
    #         video_title = video_info.get("title", "downloaded_video").replace(" ", "_")
    #         clip_duration = (end_time - start_time) if end_time is not None else video_info["duration"]

    #         # FFmpeg command for downloading only the specified clip
    #         ffmpeg_cmd = [
    #             ffmpeg_path,
    #             "-loglevel", "error",
    #             "-progress", "pipe:1",  # Output progress to stdout
    #             "-ss", str(start_time),  # Seek to start time before downloading
    #             "-t", str(clip_duration),
    #             "-i", video_url,
    #             "-ss", str(start_time),  # Seek to start time for audio
    #             "-t", str(clip_duration),
    #             "-i", audio_url,
    #             "-c:v", "copy",  # Copy video without re-encoding
    #             "-c:a", "copy",  # Copy audio without re-encoding
    #             "-y",  # Overwrite the output file if it exists
    #             os.path.join(self.download_folder, f"{video_title}_clipped.mp4"),
    #         ]

    #         print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #         # Use subprocess.Popen to capture real-time progress
    #         process = subprocess.Popen(
    #             ffmpeg_cmd,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.STDOUT,
    #             universal_newlines=True,
    #             bufsize=1,
    #         )

    #         # Track progress
    #         while process.poll() is None:
    #             if process.stdout:
    #                 for line in process.stdout:
    #                     # Parse progress from FFmpeg's output
    #                     if "out_time_ms" in line:
    #                         time_match = re.search(r"out_time_ms=(\d+)", line)
    #                         if time_match:
    #                             elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                             progress = (elapsed_time / clip_duration) * 100
    #                             if update_progress_callback:
    #                                 update_progress_callback(min(100, progress))
    #                     # Debugging: Print FFmpeg's output to check progress
    #                     print(line.strip())

    #         # Check for errors
    #         if process.returncode != 0:
    #             error_output = process.stdout.read() if process.stdout else "Unknown error"
    #             print(f"FFmpeg error: {error_output}")
    #             if update_progress_callback:
    #                 update_progress_callback(-1)  # Indicate failure with -1
    #             raise RuntimeError("FFmpeg failed to process the video.")

    #         print(f"Download completed: {os.path.join(self.download_folder, f'{video_title}_clipped.mp4')}")
    #         if update_progress_callback:
    #             update_progress_callback(100)  # Mark as complete
    #         return os.path.join(self.download_folder, f"{video_title}_clipped.mp4")

    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         if update_progress_callback:
    #             update_progress_callback(-1)  # Indicate failure with -1
    #         raise ValueError(f"An error occurred while downloading the video: {e}")






    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
    #     retries = 0
    #     while retries < max_retries:
    #         try:
    #             print(f"Starting download for URL: {url} (Attempt {retries + 1})")

    #             # Specify the location of FFmpeg
    #             ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #             # yt-dlp options for format selection
    #             ydl_opts = {
    #                 "quiet": False,
    #                 "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #                 "noplaylist": True,
    #                 "http_headers": {
    #                     "User-Agent": "Mozilla/5.0",
    #                 },
    #                 "ffmpeg_location": ffmpeg_path,
    #             }

    #             # Extract video info with yt-dlp
    #             with YoutubeDL(ydl_opts) as ydl:
    #                 video_info = ydl.extract_info(url, download=False)

    #             # Get video and audio stream URLs
    #             video_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #                 ),
    #                 key=lambda f: (
    #                     f.get("height", 0) or 0,
    #                     f.get("fps", 0) or 0
    #                 ),
    #                 default=None,
    #             )
    #             audio_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("acodec") and fmt.get("acodec") != "none"
    #                 ),
    #                 key=lambda f: f.get("abr", 0) or 0,
    #                 default=None,
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("No valid video or audio stream found.")

    #             video_url = video_stream["url"]
    #             audio_url = audio_stream["url"]

    #             # Video title and duration
    #             video_title = re.sub(r'[\\/*?:"<>|]', "_", video_info.get("title", "downloaded_video"))
    #             clip_duration = (end_time - start_time) if end_time is not None else video_info["duration"]

    #             # FFmpeg command for downloading only the specified clip
    #             output_path = os.path.join(self.download_folder, f"{video_title}_clipped.mp4")
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "error",
    #                 "-progress", "pipe:1",  # Output progress to stdout
    #                 "-ss", str(start_time),  # Seek to start time before downloading
    #                 "-t", str(clip_duration),
    #                 "-i", video_url,
    #                 "-ss", str(start_time),  # Seek to start time for audio
    #                 "-t", str(clip_duration),
    #                 "-i", audio_url,
    #                 "-c:v", "copy",  # Copy video without re-encoding
    #                 "-c:a", "copy",  # Copy audio without re-encoding
    #                 "-y",  # Overwrite the output file if it exists
    #                 output_path,
    #             ]

    #             print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #             # Use subprocess.Popen to capture real-time progress
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

    #             # Track progress
    #             while process.poll() is None:
    #                 if process.stdout:
    #                     for line in process.stdout:
    #                         if "out_time_ms" in line:
    #                             time_match = re.search(r"out_time_ms=(\d+)", line)
    #                             if time_match:
    #                                 elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                                 progress = (elapsed_time / clip_duration) * 100
    #                                 if update_progress_callback:
    #                                     update_progress_callback(min(100, progress))
    #                         print(line.strip())  # Debug FFmpeg's stdout

    #                 if process.stderr:
    #                     for line in process.stderr:
    #                         print("FFmpeg stderr:", line.strip())  # Debug FFmpeg's stderr

    #             # Check for errors
    #             if process.returncode != 0:
    #                 error_output = process.stderr.read() if process.stderr else "Unknown error"
    #                 print(f"FFmpeg error: {error_output}")
    #                 if os.path.exists(output_path):
    #                     print("Deleting incomplete file...")
    #                     os.remove(output_path)
    #                 raise RuntimeError("FFmpeg failed to process the video.")

    #             print(f"Download completed: {output_path}")
    #             if update_progress_callback:
    #                 update_progress_callback(100)  # Mark as complete
    #             return output_path

    #         except Exception as e:
    #             retries += 1
    #             if retries < max_retries:
    #                 print(f"Network error occurred. Retrying... ({retries}/{max_retries})")
    #                 time.sleep(5)  # Wait before retrying
    #             else:
    #                 print(f"Max retries reached. Failed to download the video.")
    #                 if update_progress_callback:
    #                     update_progress_callback(-1)  # Indicate failure with -1
    #                 raise ValueError(f"An error occurred while downloading the video: {e}")




    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
    #     retries = 0
    #     while retries < max_retries:
    #         try:
    #             print(f"Starting download for URL: {url} (Attempt {retries + 1})")

    #             # Specify the location of FFmpeg
    #             ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #             # yt-dlp options for format selection
    #             ydl_opts = {
    #                 "quiet": False,
    #                 "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #                 "noplaylist": True,
    #                 "http_headers": {
    #                     "User-Agent": "Mozilla/5.0",
    #                 },
    #                 "ffmpeg_location": ffmpeg_path,
    #             }

    #             # Extract video info with yt-dlp
    #             with YoutubeDL(ydl_opts) as ydl:
    #                 video_info = ydl.extract_info(url, download=False)

    #             # Get video and audio stream URLs
    #             video_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #                 ),
    #                 key=lambda f: (
    #                     f.get("height", 0) or 0,
    #                     f.get("fps", 0) or 0
    #                 ),
    #                 default=None,
    #             )
    #             audio_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("acodec") and fmt.get("acodec") != "none"
    #                 ),
    #                 key=lambda f: f.get("abr", 0) or 0,
    #                 default=None,
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("No valid video or audio stream found.")

    #             video_url = video_stream["url"]
    #             audio_url = audio_stream["url"]

    #             # Debug: Print video and audio URLs
    #             print("Video URL:", video_url)
    #             print("Audio URL:", audio_url)

    #             # Video title and duration
    #             video_title = re.sub(r'[\\/*?:"<>|]', "_", video_info.get("title", "downloaded_video"))
    #             clip_duration = (end_time - start_time) if end_time is not None else video_info["duration"]

    #             # FFmpeg command for downloading only the specified clip
    #             output_path = os.path.join(self.download_folder, f"{video_title}_clipped.mp4")
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "error",
    #                 "-progress", "pipe:1",  # Output progress to stdout
    #                 "-reconnect", "1",  # Enable reconnection
    #                 "-reconnect_streamed", "1",  # Enable reconnection for streamed inputs
    #                 "-multiple_requests", "1",  # Use separate connections for each input
    #                 "-ss", str(start_time),  # Seek to start time before downloading
    #                 "-t", str(clip_duration),
    #                 "-i", video_url,
    #                 "-ss", str(start_time),  # Seek to start time for audio
    #                 "-t", str(clip_duration),
    #                 "-i", audio_url,
    #                 "-c:v", "copy",  # Copy video without re-encoding
    #                 "-c:a", "copy",  # Copy audio without re-encoding
    #                 "-y",  # Overwrite the output file if it exists
    #                 output_path,
    #             ]

    #             print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #             # Use subprocess.Popen to capture real-time progress
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

    #             # Track progress
    #             while process.poll() is None:
    #                 if process.stdout:
    #                     for line in process.stdout:
    #                         if "out_time_ms" in line:
    #                             time_match = re.search(r"out_time_ms=(\d+)", line)
    #                             if time_match:
    #                                 elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                                 progress = (elapsed_time / clip_duration) * 100
    #                                 if update_progress_callback:
    #                                     update_progress_callback(min(100, progress))
    #                         print(line.strip())  # Debug FFmpeg's stdout

    #                 if process.stderr:
    #                     for line in process.stderr:
    #                         print("FFmpeg stderr:", line.strip())  # Debug FFmpeg's stderr

    #             # Check for errors
    #             if process.returncode != 0:
    #                 error_output = process.stderr.read() if process.stderr else "Unknown error"
    #                 print(f"FFmpeg error: {error_output}")
    #                 if os.path.exists(output_path):
    #                     print("Deleting incomplete file...")
    #                     os.remove(output_path)
    #                 raise RuntimeError("FFmpeg failed to process the video.")

    #             # Validate the output file
    #             if not os.path.exists(output_path):
    #                 raise RuntimeError("Output file not found. Download failed.")

    #             print(f"Download completed: {output_path}")
    #             if update_progress_callback:
    #                 update_progress_callback(100)  # Mark as complete
    #             return output_path

    #         except Exception as e:
    #             retries += 1
    #             if retries < max_retries:
    #                 print(f"Network error occurred. Retrying... ({retries}/{max_retries})")
    #                 time.sleep(5)  # Wait before retrying
    #             else:
    #                 print(f"Max retries reached. Failed to download the video.")
    #                 if update_progress_callback:
    #                     update_progress_callback(-1)  # Indicate failure with -1
    #                 raise ValueError(f"An error occurred while downloading the video: {e}")


    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
    #     retries = 0
    #     while retries < max_retries:
    #         try:
    #             print(f"Starting download for URL: {url} (Attempt {retries + 1})")

    #             # Specify the location of FFmpeg
    #             ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #             # yt-dlp options for format selection
    #             ydl_opts = {
    #                 "quiet": False,
    #                 "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #                 "noplaylist": True,
    #                 "http_headers": {
    #                     "User-Agent": "Mozilla/5.0",
    #                 },
    #                 "ffmpeg_location": ffmpeg_path,
    #             }

    #             # Extract video info with yt-dlp
    #             with YoutubeDL(ydl_opts) as ydl:
    #                 video_info = ydl.extract_info(url, download=False)

    #             # Get video and audio stream URLs
    #             video_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #                 ),
    #                 key=lambda f: (
    #                     f.get("height", 0) or 0,
    #                     f.get("fps", 0) or 0
    #                 ),
    #                 default=None,
    #             )
    #             audio_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("acodec") and fmt.get("acodec") != "none"
    #                 ),
    #                 key=lambda f: f.get("abr", 0) or 0,
    #                 default=None,
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("No valid video or audio stream found.")

    #             video_url = video_stream["url"]
    #             audio_url = audio_stream["url"]

    #             # Debug: Print video and audio URLs
    #             print("Video URL:", video_url)
    #             print("Audio URL:", audio_url)

    #             # Video title and duration
    #             video_title = re.sub(r'[\\/*?:"<>|]', "_", video_info.get("title", "downloaded_video"))
    #             clip_duration = (end_time - start_time) if end_time is not None else video_info["duration"]

    #             # FFmpeg command for downloading only the specified clip
    #             output_path = os.path.join(self.download_folder, f"{video_title}_clipped.mp4")
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "error",
    #                 "-progress", "pipe:1",  # Output progress to stdout
    #                 "-reconnect", "1",  # Enable reconnection
    #                 "-reconnect_streamed", "1",  # Enable reconnection for streamed inputs
    #                 "-multiple_requests", "1",  # Use separate connections for each input
    #                 "-ss", str(start_time),  # Seek to start time before downloading
    #                 "-accurate_seek",  # Add accurate seek for video
    #                 "-t", str(clip_duration),
    #                 "-i", video_url,
    #                 "-ss", str(start_time),  # Seek to start time for audio
    #                 "-accurate_seek",  # Add accurate seek for audio
    #                 "-t", str(clip_duration),
    #                 "-i", audio_url,
    #                 "-c:v", "copy",  # Copy video without re-encoding
    #                 "-c:a", "copy",  # Copy audio without re-encoding
    #                 "-f", "mp4",  # Explicitly specify the output format
    #                 "-y",  # Overwrite the output file if it exists
    #                 output_path,
    #             ]

    #             print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #             # Use subprocess.Popen to capture real-time progress
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

    #             # Track progress
    #             last_frame_time = time.time()
    #             while process.poll() is None:
    #                 if process.stdout:
    #                     for line in process.stdout:
    #                         # Check for frame=0
    #                         if "frame=0" in line:
    #                             # If frame=0 persists for 5 seconds, restart the download
    #                             if time.time() - last_frame_time > 5:
    #                                 print("FFmpeg is stuck at frame=0. Restarting download...")
    #                                 process.terminate()
    #                                 raise RuntimeError("FFmpeg is stuck at frame=0.")
    #                         else:
    #                             last_frame_time = time.time()  # Reset the timer if frames are being processed

    #                         # Parse progress from FFmpeg's output
    #                         if "out_time_ms" in line:
    #                             time_match = re.search(r"out_time_ms=(\d+)", line)
    #                             if time_match:
    #                                 elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                                 progress = (elapsed_time / clip_duration) * 100
    #                                 if update_progress_callback:
    #                                     update_progress_callback(min(100, progress))
    #                         print(line.strip())  # Debug FFmpeg's stdout

    #                 if process.stderr:
    #                     for line in process.stderr:
    #                         print("FFmpeg stderr:", line.strip())  # Debug FFmpeg's stderr

    #             # Check for errors
    #             if process.returncode != 0:
    #                 error_output = process.stderr.read() if process.stderr else "Unknown error"
    #                 print(f"FFmpeg error: {error_output}")
    #                 if os.path.exists(output_path):
    #                     print("Deleting incomplete file...")
    #                     os.remove(output_path)
    #                 raise RuntimeError("FFmpeg failed to process the video.")

    #             # Validate the output file
    #             if not os.path.exists(output_path):
    #                 raise RuntimeError("Output file not found. Download failed.")

    #             print(f"Download completed: {output_path}")
    #             if update_progress_callback:
    #                 update_progress_callback(100)  # Mark as complete
    #             return output_path

    #         except Exception as e:
    #             retries += 1
    #             if retries < max_retries:
    #                 print(f"Error occurred. Retrying... ({retries}/{max_retries})")
    #                 time.sleep(5)  # Wait before retrying
    #             else:
    #                 print(f"Max retries reached. Failed to download the video.")
    #                 if update_progress_callback:
    #                     update_progress_callback(-1)  # Indicate failure with -1
    #                 raise ValueError(f"An error occurred while downloading the video: {e}")



    # def check_ffmpeg_codecs(self, ffmpeg_path):
    #     """
    #     Check if FFmpeg supports the required codecs (H.264 for video, AAC for audio).
    #     """
    #     try:
    #         # Run ffmpeg -codecs and capture the output
    #         result = subprocess.run(
    #             [ffmpeg_path, "-codecs"],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #         )

    #         # Check if H.264 and AAC are supported
    #         if "h264" not in result.stdout.lower() or "aac" not in result.stdout.lower():
    #             raise RuntimeError("FFmpeg does not support H.264 or AAC codecs.")

    #         print("FFmpeg supports H.264 and AAC codecs.")
    #         return True

    #     except Exception as e:
    #         print(f"Error checking FFmpeg codecs: {e}")
    #         raise

    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
    #     retries = 0
    #     while retries < max_retries:
    #         try:
    #             print(f"Starting download for URL: {url} (Attempt {retries + 1})")

    #             # Specify the location of FFmpeg
    #             ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")

    #             # Check if FFmpeg supports the required codecs
    #             self.check_ffmpeg_codecs(ffmpeg_path)

    #             # yt-dlp options for format selection
    #             ydl_opts = {
    #                 "quiet": False,
    #                 "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  # Ensure best quality in MP4/M4A
    #                 "noplaylist": True,
    #                 "http_headers": {
    #                     "User-Agent": "Mozilla/5.0",
    #                 },
    #                 "ffmpeg_location": ffmpeg_path,
    #             }

    #             # Extract video info with yt-dlp
    #             with YoutubeDL(ydl_opts) as ydl:
    #                 video_info = ydl.extract_info(url, download=False)

    #             # Get video and audio stream URLs
    #             video_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("vcodec") and fmt.get("vcodec") != "none"
    #                 ),
    #                 key=lambda f: (
    #                     f.get("height", 0) or 0,
    #                     f.get("fps", 0) or 0
    #                 ),
    #                 default=None,
    #             )
    #             audio_stream = max(
    #                 (
    #                     fmt for fmt in video_info["formats"]
    #                     if fmt.get("acodec") and fmt.get("acodec") != "none"
    #                 ),
    #                 key=lambda f: f.get("abr", 0) or 0,
    #                 default=None,
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("No valid video or audio stream found.")

    #             video_url = video_stream["url"]
    #             audio_url = audio_stream["url"]

    #             # Debug: Print video and audio URLs
    #             print("Video URL:", video_url)
    #             print("Audio URL:", audio_url)

    #             # Video title and duration
    #             video_title = re.sub(r'[\\/*?:"<>|]', "_", video_info.get("title", "downloaded_video"))
    #             clip_duration = (end_time - start_time) if end_time is not None else video_info["duration"]

    #             # FFmpeg command for downloading only the specified clip
    #             output_path = os.path.join(self.download_folder, f"{video_title}_clipped.mp4")
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "error",
    #                 "-progress", "pipe:1",  # Output progress to stdout
    #                 "-reconnect", "1",  # Enable reconnection
    #                 "-reconnect_streamed", "1",  # Enable reconnection for streamed inputs
    #                 "-multiple_requests", "1",  # Use separate connections for each input
    #                 "-ss", str(start_time),  # Seek to start time before downloading
    #                 "-accurate_seek",  # Add accurate seek for video
    #                 "-t", str(clip_duration),
    #                 "-i", video_url,
    #                 "-ss", str(start_time),  # Seek to start time for audio
    #                 "-accurate_seek",  # Add accurate seek for audio
    #                 "-t", str(clip_duration),
    #                 "-i", audio_url,
    #                 "-c:v", "copy",  # Copy video without re-encoding
    #                 "-c:a", "copy",  # Copy audio without re-encoding
    #                 "-f", "mp4",  # Explicitly specify the output format
    #                 "-y",  # Overwrite the output file if it exists
    #                 output_path,
    #             ]

    #             print("Running FFmpeg command:", " ".join(ffmpeg_cmd))

    #             # Use subprocess.Popen to capture real-time progress
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

    #             # Track progress
    #             last_frame_time = time.time()
    #             while process.poll() is None:
    #                 if process.stdout:
    #                     for line in process.stdout:
    #                         # Check for frame=0
    #                         if "frame=0" in line:
    #                             # If frame=0 persists for 5 seconds, restart the download
    #                             if time.time() - last_frame_time > 5:
    #                                 print("FFmpeg is stuck at frame=0. Restarting download...")
    #                                 process.terminate()
    #                                 raise RuntimeError("FFmpeg is stuck at frame=0.")
    #                         else:
    #                             last_frame_time = time.time()  # Reset the timer if frames are being processed

    #                         # Parse progress from FFmpeg's output
    #                         if "out_time_ms" in line:
    #                             time_match = re.search(r"out_time_ms=(\d+)", line)
    #                             if time_match:
    #                                 elapsed_time = int(time_match.group(1)) / 1_000_000  # Convert ms to seconds
    #                                 progress = (elapsed_time / clip_duration) * 100
    #                                 if update_progress_callback:
    #                                     update_progress_callback(min(100, progress))
    #                         print(line.strip())  # Debug FFmpeg's stdout

    #                 if process.stderr:
    #                     for line in process.stderr:
    #                         print("FFmpeg stderr:", line.strip())  # Debug FFmpeg's stderr

    #             # Check for errors
    #             if process.returncode != 0:
    #                 error_output = process.stderr.read() if process.stderr else "Unknown error"
    #                 print(f"FFmpeg error: {error_output}")
    #                 if os.path.exists(output_path):
    #                     print("Deleting incomplete file...")
    #                     os.remove(output_path)
    #                 raise RuntimeError("FFmpeg failed to process the video.")

    #             # Validate the output file
    #             if not os.path.exists(output_path):
    #                 raise RuntimeError("Output file not found. Download failed.")

    #             print(f"Download completed: {output_path}")
    #             if update_progress_callback:
    #                 update_progress_callback(100)  # Mark as complete
    #             return output_path

    #         except Exception as e:
    #             retries += 1
    #             if retries < max_retries:
    #                 print(f"Error occurred. Retrying... ({retries}/{max_retries})")
    #                 time.sleep(5)  # Wait before retrying
    #             else:
    #                 print(f"Max retries reached. Failed to download the video.")
    #                 if update_progress_callback:
    #                     update_progress_callback(-1)  # Indicate failure with -1
    #                 raise ValueError(f"An error occurred while downloading the video: {e}")




    # def check_ffmpeg_codecs(self, ffmpeg_path):
    #     """Check FFmpeg codec support with improved validation"""
    #     try:
    #         result = subprocess.run(
    #             [ffmpeg_path, "-codecs"],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #             timeout=10
    #         )
            
    #         output = result.stdout.lower()
    #         if "h264" not in output or "aac" not in output:
    #             raise RuntimeError("Missing required codecs: H.264 or AAC")
                
    #         print("FFmpeg codec check passed")
    #         return True
            
    #     except subprocess.TimeoutExpired:
    #         raise RuntimeError("FFmpeg codec check timed out")
    #     except Exception as e:
    #         print(f"Codec check error: {e}")
    #         raise

    # def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
    #     retries = 0
    #     ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")
        
    #     while retries < max_retries:
    #         try:
    #             print(f"Download attempt {retries + 1}/{max_retries}")
    #             self.check_ffmpeg_codecs(ffmpeg_path)

    #             # Get video info with extended format handling
    #             ydl_opts = {
    #                 "quiet": True,
    #                 "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
    #                 "noplaylist": True,
    #                 "http_headers": {"User-Agent": "Mozilla/5.0"},
    #                 "ffmpeg_location": ffmpeg_path,
    #             }
                
    #             with YoutubeDL(ydl_opts) as ydl:
    #                 video_info = ydl.extract_info(url, download=False)
                
    #             # Prepare HTTP headers for FFmpeg
    #             headers = "\r\n".join(f"{k}: {v}" for k, v in ydl_opts["http_headers"].items()) + "\r\n"
                
    #             # Stream selection with fallback logic
    #             video_stream = next(
    #                 (fmt for fmt in reversed(video_info["formats"]) 
    #                     if fmt.get('vcodec') != 'none' and fmt.get('ext') == 'mp4'),
    #                 None
    #             )
    #             audio_stream = next(
    #                 (fmt for fmt in reversed(video_info["formats"])
    #                     if fmt.get('acodec') != 'none' and fmt.get('ext') in ['m4a', 'mp4']),
    #                 None
    #             )

    #             if not video_stream or not audio_stream:
    #                 raise ValueError("Suitable streams not found")

    #             # Calculate durations with safety margins
    #             clip_duration = (end_time - start_time) if end_time else video_info['duration']
    #             safe_start = max(start_time - 2, 0)  # 2-second seek buffer
    #             safe_duration = clip_duration + 2  # Extra duration buffer

    #             # FFmpeg command with multiple reliability improvements
    #             output_path = os.path.join(self.download_folder, 
    #                                         f"{re.sub(r'[\\/*?:\"<>|]', '_', video_info['title'])}.mp4")
                
    #             ffmpeg_cmd = [
    #                 ffmpeg_path,
    #                 "-loglevel", "info",
    #                 "-hide_banner",
    #                 "-y",
    #                 "-reconnect", "1",
    #                 "-reconnect_streamed", "1",
    #                 "-reconnect_delay_max", "30",
    #                 "-timeout", "30000000",
    #                 "-rw_timeout", "30000000",
    #                 # Video input with seeking improvements
    #                 "-ss", str(safe_start),
    #                 # "-noaccurate_seek",
    #                 "-i", video_stream['url'],
    #                 "-ss", str(safe_start),
    #                 # "-noaccurate_seek", 
    #                 "-i", audio_stream['url'],
    #                 # Output processing
    #                 "-t", str(safe_duration),
    #                 "-avoid_negative_ts", "make_zero",
    #                 "-fflags", "+genpts",
    #                 "-c:v", "h264_qsv",
    #                 "-c:a", "aac",  # Re-encode audio for compatibility
    #                 "-movflags", "+faststart",
    #                 "-f", "mp4",
    #                 "-progress", "pipe:1",
    #                 output_path
    #             ]

    #             # Add headers to both inputs
    #             ffmpeg_cmd[7:7] = ["-headers", headers]
    #             ffmpeg_cmd[11:11] = ["-headers", headers]

    #             # Run FFmpeg with merged output capture
    #             process = subprocess.Popen(
    #                 ffmpeg_cmd,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.STDOUT,
    #                 universal_newlines=True,
    #                 bufsize=1,
    #             )

    #             # Enhanced progress monitoring
    #             start_time = time.time()
    #             last_progress = 0
                
    #             while process.poll() is None:
    #                 line = process.stdout.readline()
    #                 if not line:
    #                     continue

    #                 # Frame stall detection
    #                 if "frame=0" in line:
    #                     if time.time() - start_time > 15:
    #                         raise RuntimeError("Frame processing timeout")
    #                 else:
    #                     start_time = time.time()

    #                 # Progress parsing
    #                 if "out_time_ms" in line:
    #                     match = re.search(r"out_time_ms=(\d+)", line)
    #                     if match:
    #                         elapsed = int(match.group(1)) / 1e6
    #                         progress = min(100, (elapsed / clip_duration) * 100)
    #                         if progress > last_progress:
    #                             if update_progress_callback:
    #                                 update_progress_callback(progress)
    #                             last_progress = progress

    #                 print(f"FFmpeg: {line.strip()}")

    #             # Post-processing checks
    #             if process.returncode != 0:
    #                 raise RuntimeError(f"FFmpeg failed with code {process.returncode}")
                    
    #             if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
    #                 raise RuntimeError("Output file validation failed")

    #             # Final trim to exact duration
    #             # self._exact_trim(output_path, start_time, clip_duration, ffmpeg_path)
                
    #             if update_progress_callback:
    #                 update_progress_callback(100)
                    
    #             return output_path

    #         except Exception as e:
    #             print(f"Attempt {retries + 1} failed: {str(e)}")
    #             retries += 1
    #             if retries < max_retries:
    #                 time.sleep(2 ** retries)  # Exponential backoff
    #             else:
    #                 # Fallback to full download + local processing
    #                 return self._fallback_download(url, start_time, end_time, ffmpeg_path)

    # def _exact_trim(self, input_path, start, duration, ffmpeg_path):
    #     """Final precise trimming using local file"""
    #     temp_path = input_path.replace(".mp4", "_temp.mp4")
        
    #     trim_cmd = [
    #         ffmpeg_path,
    #         "-y",
    #         "-i", input_path,
    #         "-ss", str(start),
    #         "-t", str(duration),
    #         "-c", "copy",
    #         "-avoid_negative_ts", "make_zero",
    #         temp_path
    #     ]
        
    #     try:
    #         subprocess.run(trim_cmd, check=True, timeout=30)
    #         os.replace(temp_path, input_path)
    #     except Exception as e:
    #         print(f"Final trim failed: {e}")
    #         if os.path.exists(temp_path):
    #             os.remove(temp_path)

    # def _fallback_download(self, url, start, end, ffmpeg_path):
    #     """Full download + local processing fallback"""
    #     print("Using fallback download method")
    #     try:
    #         with YoutubeDL({
    #             'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
    #             'format': 'bestvideo+bestaudio/best',
    #             'ffmpeg_location': ffmpeg_path
    #         }) as ydl:
    #             full_path = ydl.download([url])[0]
                
    #         # Process downloaded file
    #         output_path = full_path.replace(".", f"_trimmed_{start}-{end}.")
    #         trim_cmd = [
    #             ffmpeg_path,
    #             "-y",
    #             "-i", full_path,
    #             "-ss", str(start),
    #             "-t", str(end - start),
    #             "-c", "copy",
    #             output_path
    #         ]
    #         subprocess.run(trim_cmd, check=True)
    #         return output_path
    #     except Exception as e:
    #         raise RuntimeError(f"Fallback method failed: {e}")

 
#######################################################################################

#     def check_ffmpeg_codecs(self, ffmpeg_path):
#         """Check FFmpeg codec support with improved validation"""
#         try:
#             result = subprocess.run(
#                 [ffmpeg_path, "-codecs"],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 universal_newlines=True,
#                 timeout=10
#             )
            
#             output = result.stdout.lower()
#             if "h264" not in output or "aac" not in output:
#                 raise RuntimeError("Missing required codecs: H.264 or AAC")
                
#             print("FFmpeg codec check passed")
#             return True
            
#         except subprocess.TimeoutExpired:
#             raise RuntimeError("FFmpeg codec check timed out")
#         except Exception as e:
#             print(f"Codec check error: {e}")
#             raise

#     def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
#         retries = 0
#         ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")
        
#         while retries < max_retries:
#             try:
#                 print(f"Download attempt {retries + 1}/{max_retries}")
#                 self.check_ffmpeg_codecs(ffmpeg_path)

#                 # Get video info with extended format handling
#                 ydl_opts = {
#                     "quiet": True,
#                     "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
#                     "noplaylist": True,
#                     "http_headers": {"User-Agent": "Mozilla/5.0"},
#                     "ffmpeg_location": ffmpeg_path,
#                 }
                
#                 with YoutubeDL(ydl_opts) as ydl:
#                     video_info = ydl.extract_info(url, download=False)
                
#                 # Prepare HTTP headers for FFmpeg
#                 headers = "\r\n".join(f"{k}: {v}" for k, v in ydl_opts["http_headers"].items()) + "\r\n"
                
#                 # Stream selection with extended format support
#                 video_stream = next(
#                     (fmt for fmt in reversed(video_info["formats"]) 
#                         if fmt.get('vcodec') != 'none' and fmt.get('protocol') in ['http', 'https']),
#                     None
#                 )
#                 audio_stream = next(
#                     (fmt for fmt in reversed(video_info["formats"])
#                         if fmt.get('acodec') != 'none' and fmt.get('protocol') in ['http', 'https']),
#                     None
#                 )

#                 if not video_stream or not audio_stream:
#                     raise ValueError("Suitable streams not found")

#                 # Calculate durations with safety margins
#                 clip_duration = (end_time - start_time) if end_time else video_info['duration']
#                 safe_start = max(start_time - 2, 0)  # 2-second seek buffer
#                 safe_duration = clip_duration + 2  # Extra duration buffer

#                 # FFmpeg command with broader compatibility
#                 output_path = os.path.join(self.download_folder, 
#                                             f"{re.sub(r'[\\/*?:\"<>|]', '_', video_info['title'])}.mp4")
                
#                 ffmpeg_cmd = [
#                     ffmpeg_path,
#                     "-loglevel", "info",
#                     "-hide_banner",
#                     "-y",
#                     "-reconnect", "1",
#                     "-reconnect_streamed", "1",
#                     "-reconnect_delay_max", "30",
#                     "-timeout", "30000000",
#                     "-rw_timeout", "30000000",
#                     "-ss", str(safe_start),
#                     "-i", video_stream['url'],
#                     "-ss", str(safe_start),
#                     "-i", audio_stream['url'],
#                     "-t", str(safe_duration),
#                     "-avoid_negative_ts", "make_zero",
#                     "-fflags", "+genpts",
#                     # "-c:v", "h264_qsv",  # Using a more flexible codec h264_nvenc
#                     "-c:v", "h264_nvenc",  # Using a more flexible codec h264_nvenc
#                     "-c:a", "aac",
#                     "-movflags", "+faststart",
#                     "-f", "mp4",
#                     "-progress", "pipe:1",
#                     output_path
#                 ]

#                 # Add headers to both inputs
#                 ffmpeg_cmd[7:7] = ["-headers", headers]
#                 ffmpeg_cmd[11:11] = ["-headers", headers]

#                 # Run FFmpeg with merged output capture
#                 process = subprocess.Popen(
#                     ffmpeg_cmd,
#                     stdout=subprocess.PIPE,
#                     stderr=subprocess.STDOUT,
#                     universal_newlines=True,
#                     bufsize=1,
#                 )

#                 # Enhanced progress monitoring
#                 start_time = time.time()
#                 last_progress = 0
                
#                 while process.poll() is None:
#                     line = process.stdout.readline()
#                     if not line:
#                         continue

#                     # Frame stall detection
#                     if "frame=0" in line:
#                         if time.time() - start_time > 15:
#                             raise RuntimeError("Frame processing timeout")
#                     else:
#                         start_time = time.time()

#                     # Progress parsing
#                     if "out_time_ms" in line:
#                         match = re.search(r"out_time_ms=(\d+)", line)
#                         if match:
#                             elapsed = int(match.group(1)) / 1e6
#                             progress = min(100, (elapsed / clip_duration) * 100)
#                             if progress > last_progress:
#                                 if update_progress_callback:
#                                     update_progress_callback(progress)
#                                 last_progress = progress

#                     print(f"FFmpeg: {line.strip()}")

#                 # Post-processing checks
#                 if process.returncode != 0:
#                     raise RuntimeError(f"FFmpeg failed with code {process.returncode}")
                    
#                 if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
#                     raise RuntimeError("Output file validation failed")

#                 # Final trim to exact duration (if needed)
#                 # self._exact_trim(output_path, start_time, clip_duration, ffmpeg_path)
                
#                 if update_progress_callback:
#                     update_progress_callback(100)
                    
#                 return output_path

#             except Exception as e:
#                 print(f"Attempt {retries + 1} failed: {str(e)}")
#                 retries += 1
#                 if retries < max_retries:
#                     time.sleep(2 ** retries)  # Exponential backoff
#                 else:
#                     return self._fallback_download(url, start_time, end_time, ffmpeg_path)

#     def _exact_trim(self, input_path, start, duration, ffmpeg_path):
#         """Final precise trimming using local file"""
#         temp_path = input_path.replace(".mp4", "_temp.mp4")
        
#         trim_cmd = [
#             ffmpeg_path,
#             "-y",
#             "-i", input_path,
#             "-ss", str(start),
#             "-t", str(duration),
#             "-c", "copy",
#             "-avoid_negative_ts", "make_zero",
#             temp_path
#         ]
        
#         try:
#             subprocess.run(trim_cmd, check=True, timeout=30)
#             os.replace(temp_path, input_path)
#         except Exception as e:
#             print(f"Final trim failed: {e}")
#             if os.path.exists(temp_path):
#                 os.remove(temp_path)

#     def _fallback_download(self, url, start, end, ffmpeg_path):
#         """Full download + local processing fallback"""
#         print("Using fallback download method")
#         try:
#             with YoutubeDL({
#                 'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
#                 'format': 'bestvideo+bestaudio/best',
#                 'ffmpeg_location': ffmpeg_path
#             }) as ydl:
#                 full_path = ydl.download([url])[0]
                
#             # Process downloaded file
#             output_path = full_path.replace(".", f"_trimmed_{start}-{end}.")
#             trim_cmd = [
#                 ffmpeg_path,
#                 "-y",
#                 "-i", full_path,
#                 "-ss", str(start),
#                 "-t", str(end - start),
#                 "-c", "copy",
#                 output_path
#             ]
#             subprocess.run(trim_cmd, check=True)
#             return output_path
#         except Exception as e:
#             raise RuntimeError(f"Fallback method failed: {e}")

# #######################################################################################
 
import os
import subprocess
from yt_dlp import YoutubeDL
import re
import psutil
import time

class VideoDownloader:
    def __init__(self):
        self.download_folder = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_folder, exist_ok=True)
    def _timestamp_to_sec(self, timestamp):
        """Convert timestamp string (HH:MM:SS, MM:SS, or SS) to seconds"""
        try:
            parts = list(map(int, timestamp.split(':')))
            if len(parts) == 3:  # HH:MM:SS format
                hours, minutes, seconds = parts
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:  # MM:SS format
                minutes, seconds = parts
                return minutes * 60 + seconds
            elif len(parts) == 1:  # SS format
                return parts[0]
            else:
                raise ValueError("Invalid timestamp format")
        except ValueError as e:
            raise ValueError(f"Invalid timestamp '{timestamp}': {e}")

    def check_ffmpeg_codecs(self, ffmpeg_path):
        """Check FFmpeg codec support with improved validation"""
        try:
            result = subprocess.run(
                [ffmpeg_path, "-codecs"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=10
            )
            
            output = result.stdout.lower()
            if "h264" not in output or "aac" not in output:
                raise RuntimeError("Missing required codecs: H.264 or AAC")
                
            print("FFmpeg codec check passed")
            return True
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("FFmpeg codec check timed out")
        except Exception as e:
            print(f"Codec check error: {e}")
            raise

    def download_video(self, url, start_time=0, end_time=None, update_progress_callback=None, max_retries=3):
        # Convert timestamp strings to seconds
        try:
            if isinstance(start_time, str):
                start_time = self._timestamp_to_sec(start_time)
            if end_time is not None and isinstance(end_time, str):
                end_time = self._timestamp_to_sec(end_time)
        except ValueError as e:
            raise ValueError(f"Timestamp conversion error: {e}")

        retries = 0
        ffmpeg_path = os.path.join(os.getcwd(), "libs", "ffmpeg", "bin", "ffmpeg.exe")
        
        while retries < max_retries:
            try:
                print(f"Download attempt {retries + 1}/{max_retries}")
                self.check_ffmpeg_codecs(ffmpeg_path)

                # Get video info with extended format handling
                # ydl_opts = {
                #     "quiet": True,
                #     "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                #     "noplaylist": True,
                #     "http_headers": {"User-Agent": "Mozilla/5.0"},
                #     "ffmpeg_location": ffmpeg_path,
                # }
                ydl_opts = {
                    "quiet": True,
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                    "noplaylist": True,
                    "http_headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Referer": "https://www.youtube.com/",
                        "Cookie": "YOUR_NEW_COOKIES_HERE22"
                    },
                    "ffmpeg_location": ffmpeg_path,
                }
                

                with YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(url, download=False)
                
                # Prepare HTTP headers for FFmpeg
                headers = "\r\n".join(f"{k}: {v}" for k, v in ydl_opts["http_headers"].items()) + "\r\n"
                
                # Stream selection with extended format support
                video_stream = next(
                    (fmt for fmt in reversed(video_info["formats"]) 
                        if fmt.get('vcodec') != 'none' and fmt.get('protocol') in ['http', 'https']),
                    None
                )
                audio_stream = next(
                    (fmt for fmt in reversed(video_info["formats"])
                        if fmt.get('acodec') != 'none' and fmt.get('protocol') in ['http', 'https']),
                    None
                )

                if not video_stream or not audio_stream:
                    raise ValueError("Suitable streams not found")

                # Calculate durations with safety margins
                clip_duration = (end_time - start_time) if end_time else video_info['duration']
                safe_start = max(start_time - 2, 0)  # 2-second seek buffer
                safe_duration = clip_duration + 2  # Extra duration buffer

                # FFmpeg command with broader compatibility
                # output_path = os.path.join(self.download_folder, 
                #                             f"{re.sub(r'[^\w\s-]', '_', video_info['title'])}.mp4")


                #this is to not overwrite if there is exsisting video 
                # FFmpeg command with broader compatibility
                base_filename = re.sub(r'[^\w\s-]', '_', video_info['title'])
                output_path = os.path.join(self.download_folder, f"{base_filename}.mp4")

                # Check for duplicates and modify filename if needed
                counter = 1
                while os.path.exists(output_path):
                    output_path = os.path.join(self.download_folder, f"{base_filename}_{counter}.mp4")
                    counter += 1


                
                # ffmpeg_cmd = [
                #     ffmpeg_path,
                #     "-loglevel", "info",
                #     "-hide_banner",
                #     "-y",
                #     "-reconnect", "1",
                #     "-reconnect_streamed", "1",
                #     "-reconnect_delay_max", "30",
                #     "-timeout", "30000000",
                #     "-rw_timeout", "30000000",
                #     "-ss", str(safe_start),
                #     "-i", video_stream['url'],
                #     "-ss", str(safe_start),
                #     "-i", audio_stream['url'],
                #     "-t", str(safe_duration),
                #     "-avoid_negative_ts", "make_zero",
                #     "-fflags", "+genpts",
                #     "-c:v", "h264_nvenc",
                #     "-c:a", "aac",
                #     "-movflags", "+faststart",
                #     "-f", "mp4",
                #     "-progress", "pipe:1",
                #     output_path
                # ]

                ffmpeg_cmd = [
                ffmpeg_path,
                "-loglevel", "info",
                "-hide_banner",
                "-y",
                "-reconnect", "1",
                "-reconnect_streamed", "1",
                "-reconnect_delay_max", "30",
                "-timeout", "30000000",
                "-rw_timeout", "30000000",
                "-ss", str(safe_start),
                "-i", video_stream['url'],
                "-ss", str(safe_start),
                "-i", audio_stream['url'],
                "-t", str(safe_duration),
                "-avoid_negative_ts", "make_zero",
                "-fflags", "+genpts",
                "-c:v", "h264_nvenc",
                "-b:v", "12M",  # Average bitrate
                "-maxrate:v", "16M",  # Maximum bitrate
                "-bufsize:v", "24M",  # Buffer size (1.5-2x maxrate)
                "-rc:v", "vbr_hq",  # High quality variable bitrate
                "-preset:v", "hq",  # Quality preset
                "-cq:v", "18",  # Quality level (18-23, lower=better)
                "-c:a", "aac",
                "-b:a", "192k",  # Audio bitrate
                "-movflags", "+faststart",
                "-f", "mp4",
                "-progress", "pipe:1",
                output_path
                ]

                # Add headers to both inputs
                ffmpeg_cmd[7:7] = ["-headers", headers]
                ffmpeg_cmd[11:11] = ["-headers", headers]

                # Run FFmpeg with merged output capture
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1,
                )

                # Enhanced progress monitoring
                start_time = time.time()
                last_progress = 0
                
                while process.poll() is None:
                    line = process.stdout.readline()
                    if not line:
                        continue

                    # Frame stall detection
                    if "frame=0" in line:
                        if time.time() - start_time > 15:
                            raise RuntimeError("Frame processing timeout")
                    else:
                        start_time = time.time()

                    # Progress parsing
                    if "out_time_ms" in line:
                        match = re.search(r"out_time_ms=(\d+)", line)
                        if match:
                            elapsed = int(match.group(1)) / 1e6
                            progress = min(100, (elapsed / clip_duration) * 100)
                            if progress > last_progress:
                                if update_progress_callback:
                                    update_progress_callback(progress)
                                last_progress = progress

                    print(f"FFmpeg: {line.strip()}")

                # Post-processing checks
                if process.returncode != 0:
                    raise RuntimeError(f"FFmpeg failed with code {process.returncode}")
                    
                if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
                    raise RuntimeError("Output file validation failed")

                # Final trim to exact duration (if needed)
                # self._exact_trim(output_path, start_time, clip_duration, ffmpeg_path)
                
                if update_progress_callback:
                    update_progress_callback(100)
                    
                return output_path

            except Exception as e:
                print(f"Attempt {retries + 1} failed: {str(e)}")
                retries += 1
                if retries < max_retries:
                    time.sleep(2 ** retries)  # Exponential backoff
                else:
                    return self._fallback_download(url, start_time, end_time, ffmpeg_path)

    def _exact_trim(self, input_path, start, duration, ffmpeg_path):
        """Final precise trimming using local file"""
        temp_path = input_path.replace(".mp4", "_temp.mp4")
        
        trim_cmd = [
            ffmpeg_path,
            "-y",
            "-i", input_path,
            "-ss", str(start),
            "-t", str(duration),
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            temp_path
        ]
        
        try:
            subprocess.run(trim_cmd, check=True, timeout=30)
            os.replace(temp_path, input_path)
        except Exception as e:
            print(f"Final trim failed: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _fallback_download(self, url, start, end, ffmpeg_path):
        """Full download + local processing fallback"""
        print("Using fallback download method")
        try:
            with YoutubeDL({
                'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'ffmpeg_location': ffmpeg_path
            }) as ydl:
                full_path = ydl.download([url])[0]
                
            # Process downloaded file
            output_path = full_path.replace(".", f"_trimmed_{start}-{end}.")
            trim_cmd = [
                ffmpeg_path,
                "-y",
                "-i", full_path,
                "-ss", str(start),
                "-t", str(end - start),
                "-c", "copy",
                output_path
            ]
            subprocess.run(trim_cmd, check=True)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Fallback method failed: {e}")