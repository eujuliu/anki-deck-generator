def format_meaning(meaning: str):
    if meaning.find(";"):
        return meaning.split(";")[0] + "."

    return meaning
