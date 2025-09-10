from formula_1_etl.utils.build_endpoint import build_endpoint


def test_build_endpoint_category():
    category = "seasons"
    endpoint = build_endpoint(category=category)
    assert "seasons" == endpoint


def test_build_endpoint_category_season():
    category = "seasons"
    season = "2025"
    endpoint = build_endpoint(category=category, season=season)
    assert "2025/seasons" == endpoint
