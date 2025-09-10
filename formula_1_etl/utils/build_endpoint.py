def build_endpoint(category, season=None, rounds=None):
    pieces = []
    if season:
        pieces.append(season)

    if rounds:
        pieces.append(rounds)

    pieces.append(category)
    return "/".join(pieces)
