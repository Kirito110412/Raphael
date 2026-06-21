def build_prompt(role: str, context: dict) -> str:
    return f"Role: {role}\nContext: {context}"
