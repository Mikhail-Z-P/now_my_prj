import pytest
from unittest.mock import patch, mock_open
from src.utils import load_transactions, process_transaction
import json
import os

def test_file_does_not_exist():
    """Тест: файл не существует → вернуть пустой список."""
    with patch('os.path.exists', return_value=False):
        result = load_transactions('nonexistent.json')
        assert result == []

def test_empty_json_array():
    """Тест: пустой JSON‑массив → вернуть пустой список."""
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data='[]')):
        result = load_transactions('empty.json')
        assert result == []

def test_valid_json_array():
    """Тест: валидный JSON‑массив → вернуть список транзакций."""
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data='[{"amount": 100, "currency": "RUB"}]')):
        result = load_transactions('valid.json')
        expected = [{"amount": 100, "currency": "RUB"}]
        assert result == expected

def test_json_is_not_list():
    """Тест: JSON — объект, а не массив → вернуть пустой список."""
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data='{"key": "value"}')):
        result = load_transactions('object.json')
        assert result == []

def test_io_error_during_file_opening():
    """Тест: ошибка IO при открытии файла → вернуть пустой список."""
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', side_effect=IOError('File error')):
        result = load_transactions('error.json')
        assert result == []

def test_json_decode_error():
    """Тест: некорректный JSON → вернуть пустой список."""
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data='malformed json')):
        result = load_transactions('malformed.json')
        assert result == []


def test_rub_transaction():
    """Тест: транзакция в RUB → вернуть сумму без изменений."""
    transaction = {'amount': 1000, 'currency': 'RUB'}
    result = process_transaction(transaction)
    assert result == 1000.0


def test_missing_amount():
    """Тест: отсутствует 'amount' → вызвать ValueError."""
    transaction = {'currency': 'USD'}
    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)
    assert 'Транзакция должна содержать \'amount\' и \'currency\'' in str(exc_info.value)

def test_missing_currency():
    """Тест: отсутствует 'currency' → вызвать ValueError."""
    transaction = {'amount': 100}
    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)
    assert 'Транзакция должна содержать \'amount\' и \'currency\'' in str(exc_info.value)

def test_invalid_amount_type():
    """Тест: 'amount' не число → вызвать ValueError."""
    transaction = {'amount': '100', 'currency': 'USD'}
    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)
    assert 'Сумма должна быть числом' in str(exc_info.value)

def test_unsupported_currency():
    """Тест: неподдерживаемая валюта → вызвать ValueError."""
    transaction = {'amount': 100, 'currency': 'GBP'}
    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)
    assert 'Неподдерживаемая валюта' in str(exc_info.value)

def test_negative_amount():
    """Тест: отрицательная сумма → обработать корректно."""
    transaction = {'amount': -50, 'currency': 'RUB'}
    result = process_transaction(transaction)
    assert result == -50.0
