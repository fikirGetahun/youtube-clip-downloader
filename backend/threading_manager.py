 


import threading
import psutil
from queue import Queue

class ThreadingManager:
    def __init__(self):
        self.download_queue = Queue()
        self.active_threads = []

    def add_task(self, target, args=()):
        """Add a download task to the queue."""
        self.download_queue.put((target, args))

    def start_downloads(self, max_threads=3):
        """Start the download tasks using multiple threads, limiting CPU usage."""
        while not self.download_queue.empty() and len(self.active_threads) < max_threads:
            target, args = self.download_queue.get()
            thread = threading.Thread(target=self._thread_wrapper, args=(target, args), daemon=True)
            thread.start()
            self.active_threads.append(thread)

    def _thread_wrapper(self, target, args):
        """Wrapper to handle thread execution, including limiting CPU usage."""
        try:
            # Get the current thread's ID and set its CPU affinity to a specific core
            thread = threading.current_thread()
            self._limit_cpu_usage(thread)

            # Execute the target function (download task)
            target(*args)
        finally:
            self._remove_completed_thread()

    def _remove_completed_thread(self):
        """Remove completed threads from the active threads list."""
        self.active_threads = [t for t in self.active_threads if t.is_alive()]

    def is_all_done(self):
        """Check if all download tasks are done."""
        return self.download_queue.empty() and all(not t.is_alive() for t in self.active_threads)

    def _limit_cpu_usage(self, thread):
        """Limit CPU usage of the thread by setting its CPU affinity."""
        try:
            # Assign the thread to a specific CPU core to control CPU usage
            # Here, we use only one or two cores to limit CPU load (cores 0 and 1 in this case)
            p = psutil.Process(thread.ident)
            p.cpu_affinity([0, 1])  # Assign thread to CPU cores 0 and 1
            p.nice(psutil.IDLE_PRIORITY_CLASS)  # Set the thread's priority to low
        except Exception as e:
            print(f"Error limiting CPU usage for thread {thread.name}: {e}")



# import threading
# from queue import Queue

# class ThreadingManager:
    # def __init__(self):
        # self.download_queue = Queue()
        # self.active_threads = []

    # def add_task(self, target, args=()):
        # self.download_queue.put((target, args))

    # def start_downloads(self, max_threads=3):
        # while not self.download_queue.empty() and len(self.active_threads) < max_threads:
            # target, args = self.download_queue.get()
            # thread = threading.Thread(target=self._thread_wrapper, args=(target, args), daemon=True)
            # thread.start()
            # self.active_threads.append(thread)

    # def _thread_wrapper(self, target, args):
        # try:
            # target(*args)
        # finally:
            # self._remove_completed_thread()

    # def _remove_completed_thread(self):
        # self.active_threads = [t for t in self.active_threads if t.is_alive()]

    # def is_all_done(self):
        # return self.download_queue.empty() and all(not t.is_alive() for t in self.active_threads)
