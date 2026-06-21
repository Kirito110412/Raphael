class ConversationStateTracker:
    def __init__(self):
        self.history = []

    def add_state(self, state: dict):
        self.history.append(state)

    def get_recent_states(self, n: int = 5) -> list:
        return self.history[-n:]
