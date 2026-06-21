class SkillRegistry:
    def __init__(self):
        self.skills = {}

    def register_skill(self, skill_id: str, metadata: dict):
        self.skills[skill_id] = metadata

    def get_skill(self, skill_id: str) -> dict:
        return self.skills.get(skill_id)
