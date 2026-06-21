class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id):
        return self.sessions.get(session_id, {})

    def update_session(self, session_id, data):
        self.sessions[session_id] = data
