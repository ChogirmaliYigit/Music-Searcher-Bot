from fuzzywuzzy import fuzz


def search(text, data):
    result = []
    for item in data:
        similarity = fuzz.ratio(text.lower(), item.lower())
        result.append(similarity)
    return result
