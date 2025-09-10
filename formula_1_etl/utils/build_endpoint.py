def build_endpoint(category, season=None):
    pieces = []
    if season:
        pieces.append(season)
    pieces.append(category)
    return "/".join(pieces)
