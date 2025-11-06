def process_data(data):
    try:
        items = list(data)
    except TypeError:
        raise TypeError("data must be an iterable") from None
    if not all(isinstance(item, (int, float)) for item in items):
        raise TypeError("all items in data must be int or float")
    return [item * 2 for item in items]
