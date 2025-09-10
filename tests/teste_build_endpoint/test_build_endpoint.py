from formula_1_etl.utils.build_endpoint import build_endpoint


def test_build_endpoint_category():
    category = "seasons"
    endpoint = build_endpoint(category=category)
    return endpoint
