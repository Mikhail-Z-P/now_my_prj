from unittest.mock import patch

import pandas as pd

from src.tables_pandas import reading_csv, reading_excel


def test_successful_reading_with_mock():
    """Тест успешного чтения CSV с моком"""
    test_data = pd.DataFrame({"transaction_id": [1, 2], "amount": [100.0, 200.0], "currency": ["USD", "EUR"]})
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.return_value = test_data

        result = reading_csv("dummy_path.csv")

        mock_read_csv.assert_called_once_with("dummy_path.csv")
        assert result == [
            {"transaction_id": 1, "amount": 100.0, "currency": "USD"},
            {"transaction_id": 2, "amount": 200.0, "currency": "EUR"},
        ]


def test_file_not_found_with_patch():
    """Тест обработки ошибки FileNotFoundError с patch"""
    with patch("pandas.read_csv", side_effect=FileNotFoundError("File not found")):
        result = reading_csv("non_existent.csv")
        assert result == []


def test_other_exception_with_patch():
    """Тест обработки других исключений"""
    with patch("pandas.read_csv", side_effect=Exception("Some error")):
        result = reading_csv("problematic.csv")
        assert result == []


def test_successful_reading_excel_with_mock():
    """Тест успешного чтения Excel с моком"""
    test_data = pd.DataFrame(
        {
            "transaction_id": [101, 102],
            "amount": [150.0, 300.0],
            "category": ["Groceries", "Entertainment"],
            "date": ["2023-01-15", "2023-01-20"],
        }
    )
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_data

        result = reading_excel("dummy_path.xlsx")

        mock_read_excel.assert_called_once_with("dummy_path.xlsx")
        assert result == [
            {"transaction_id": 101, "amount": 150.0, "category": "Groceries", "date": "2023-01-15"},
            {"transaction_id": 102, "amount": 300.0, "category": "Entertainment", "date": "2023-01-20"},
        ]


def test_excel_file_not_found_with_patch():
    """Тест обработки ошибки FileNotFoundError с patch для Excel"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")):
        result = reading_excel("non_existent.xlsx")
        assert result == []


def test_other_exception_excel_with_patch():
    """Тест обработки других исключений для Excel"""
    with patch("pandas.read_excel", side_effect=Exception("Some Excel error")):
        result = reading_excel("problematic.xlsx")
        assert result == []
