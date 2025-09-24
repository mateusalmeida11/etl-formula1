from datetime import datetime


def create_root_path(layer_name, category):
    today = datetime.today()
    return (
        f"{layer_name}/{category}/year={today.year}/month={today.month}/day={today.day}"
    )


def create_file_name(category, season=None):
    path_file = category
    if season:
        path_file += f"_{season}"
    return path_file
