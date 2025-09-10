from datetime import datetime

from formula_1_etl.utils.create_name_files import create_root_path


def test_root_path_name_layers():
    layer = "bronze"
    category = "races"
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day

    result = create_root_path(layer_name=layer, category=category)

    expected = f"{layer}/{category}/year={year}/month={month}/day={day}"

    assert expected == result
