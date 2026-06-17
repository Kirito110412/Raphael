import queue
import threading

# Thread-safe queue for background agents to push results to foreground
background_queue = queue.Queue()

class BackgroundManager:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        # Future: start asyncio background loop for background agents

    def stop(self):
        self.running = False
