import json


def save_json(data, path=r"assets/settings.json", mode='w'):
    with open(path, mode) as outfile:
        json.dump(
            data,
            outfile,
            sort_keys=False,
            indent=4
        )


def read_json(path=r"assets/settings.json"):
    file = open(path)
    content = json.load(file)
    file.close()
    return content
