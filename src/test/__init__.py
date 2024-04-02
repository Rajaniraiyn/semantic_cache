from semantic_cache import semantic_cache


@semantic_cache()
def say(message: str) -> str:
    return f"Hi {message}"
