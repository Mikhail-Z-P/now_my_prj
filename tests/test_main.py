from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from main import start_processing


@pytest.fixture
def test_data():
    """Тестовые данные для загрузки."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "description": "Оплата интернета",
            "from": "Visa 1234",
            "to": "MasterCard 5678",
            "amount": 1000,
            "currency_name": "RUB",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2023-01-02T11:00:00",
            "description": "Перевод другу",
            "from": "",
            "to": "MasterCard 9012",
            "amount": 500,
            "currency_code": "USD",
        },
    ]


@patch("builtins.input", side_effect=["1", "dummy.json", "EXECUTED", "нет", "по возрастанию", "нет", "нет"])
@patch("builtins.print")
@patch("json.load")
def test_start_processing_json(mock_json_load, mock_print, test_data):
    """Проверяет загрузку данных из JSON-файла."""
    mock_json_load.return_value = test_data

    with patch("builtins.open", mock_open(read_data="dummy")):
        start_processing()

    assert mock_json_load.called


@patch("builtins.input", side_effect=["2", "dummy.csv", "EXECUTED", "нет", "по возрастанию", "нет", "нет"])
@patch("builtins.print")
def test_start_processing_csv(mock_print, test_data):
    """Проверяет загрузку данных из CSV-файла."""
    data_iter = iter(test_data)

    with (
        patch("csv.DictReader", return_value=data_iter),
        patch("builtins.open", mock_open(read_data="id,state\n1,EXECUTED")),
    ):
        start_processing()


@patch("builtins.input", side_effect=["3", "dummy.xlsx", "EXECUTED", "нет", "по возрастанию", "нет", "нет"])
@patch("builtins.print")
@patch("pandas.read_excel")
def test_start_processing_xlsx(mock_read_excel, mock_print, test_data):
    """Проверяет загрузку данных из XLSX-файла."""
    df = pd.DataFrame(test_data)
    mock_read_excel.return_value = df

    start_processing()
    assert mock_read_excel.called


@patch("builtins.input", side_effect=["1", "dummy.json", "EXECUTED", "нет", "по возрастанию", "нет", "нет"])
@patch("builtins.print")
@patch("json.load")
def test_start_processing_filter_executed(mock_json_load, mock_print, test_data):
    """Проверяет фильтрацию по статусу EXECUTED."""
    mock_json_load.return_value = test_data

    with patch("builtins.open", mock_open(read_data="dummy")):
        start_processing()

    executed_calls = [
        call for call in mock_print.call_args_list if 'Операции отфильтрованы по статусу "EXECUTED"' in str(call)
    ]
    assert len(executed_calls) > 0
