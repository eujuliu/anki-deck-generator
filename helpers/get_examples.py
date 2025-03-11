def get_examples(data: dict):
    examples = []
    for meaning in data["meanings"]:
        for definition in meaning["definitions"]:
            example = definition.get("example", None)
            if example:
                examples.append(definition["example"])

    return examples
