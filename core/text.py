import unicodedata

def normalize_search(text: str) -> str:
    return unicodedata.normalize("NFC", text).strip().casefold()