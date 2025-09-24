from datetime import datetime

from formula_1_etl.utils.create_name_files import create_file_name, create_root_path


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


def test_file_name_season():
    category = "driveres"
    season = "2025"

    result = create_file_name(category=category, season=season)
    expected = f"{category}_{season}"
    assert result == expected
