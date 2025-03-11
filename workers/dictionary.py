from helpers.fetch import fetch
from helpers.get_examples import get_examples
from helpers.format_meaning import format_meaning


def dictionary(word: str, language: str) -> dict:
    data = fetch(f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}")

    if isinstance(data, Exception):
        return Exception("Word not found")

    meaning = format_meaning(data[0]["meanings"][0]["definitions"][0]["definition"])
    example = get_examples(data[0])[0]

    return {
        "word": word,
        "meaning": meaning,
        "example": example,
    }
