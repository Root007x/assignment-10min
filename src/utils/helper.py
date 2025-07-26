import json


def save_data(data):
    with open("data/book_data.json", "w", encoding="utf-8") as file:
        file.write(data)
