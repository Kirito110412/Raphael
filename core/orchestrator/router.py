from semantic_router import Route, RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

# Define routes based on PRD Section 4.2 domain agents
# Note: For Hinglish vectors, a specific encoder model would be used in prod
# [IMPLEMENTATION_DETAIL: Using standard HuggingFaceEncoder for stub/test]
try:
    encoder = HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")

    security = Route(name="security", utterances=["scan network", "check vulnerability", "pentest"])
    finance = Route(name="finance", utterances=["buy stock", "tax calculation", "portfolio"])
    content = Route(name="content", utterances=["write script", "edit video", "post to social"])
    research = Route(name="research", utterances=["deep dive", "academic paper", "literature review"])
    tutoring = Route(name="tutoring", utterances=["teach me", "explain", "how does it work"])
    digital_worker = Route(name="digital_worker", utterances=["send email", "schedule meeting", "fill form"])
    discovery = Route(name="discovery", utterances=["invent", "novel solution", "Level 6"])
    health = Route(name="health", utterances=["symptoms", "doctor appointment", "medication"])
    legal = Route(name="legal", utterances=["contract analysis", "compliance", "law"])
    travel = Route(name="travel", utterances=["book flight", "visa requirements", "itinerary"])
    negotiation = Route(name="negotiation", utterances=["coach me", "salary discussion", "negotiate"])
    conversation = Route(name="conversation", utterances=["hi", "how are you", "what's up"])

    routes = [security, finance, content, research, tutoring, digital_worker,
              discovery, health, legal, travel, negotiation, conversation]

    route_layer = RouteLayer(encoder=encoder, routes=routes)
except Exception:
    route_layer = None

def classify_intent(text: str) -> str:
    """Uses semantic-router for intent classification"""
    if route_layer:
        result = route_layer(text)
        if result.name:
            return result.name
    return "conversation" # fallback

def get_complexity_score(text: str) -> float:
    """Stub for routeLLM complexity scoring (0.0 - 1.0)"""
    from core.inference.complexity_classifier import classify_complexity
    return classify_complexity(text)
