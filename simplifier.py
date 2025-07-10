import re

def simplify_text(text):
    # 1. Convert to lowercase
    text = text.lower()

    # 2. Replace difficult words with simpler ones (very basic example)
    replacements = {
        "utilize": "use",
        "approximately": "about",
        "commence": "start",
        "terminate": "end",
        "assistance": "help"
    }

    for word, simple_word in replacements.items():
        text = re.sub(rf'\b{word}\b', simple_word, text)

    # 3. Remove unnecessary punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # 4. Trim extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text
