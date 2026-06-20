class BackgroundEventBus:
    def __init__(self):
        self.events = []

    def dispatch(self, event: dict):
        self.events.append(event)
