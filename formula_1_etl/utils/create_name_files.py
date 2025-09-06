from datetime import datetime


def create_root_path(layer_name, endpoint):
    today = datetime.today()
    return f"{layer_name}/{endpoint}/{today.year}/{today.month}/{today.day}"
