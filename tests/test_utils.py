from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions, process_transaction


def test_file_does_not_exist():
    """Тест: файл не существует → вернуть пустой список."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions("nonexistent.json")
        assert result == []


def test_empty_json_array():
    """Тест: пустой JSON‑массив → вернуть пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="[]")):
        result = load_transactions("empty.json")
        assert result == []


def test_valid_json_array():
    """Тест: валидный JSON‑массив → вернуть список транзакций."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data='[{"amount": 100, "currency": "RUB"}]')),
    ):
        result = load_transactions("valid.json")
        expected = [{"amount": 100, "currency": "RUB"}]
        assert result == expected


def test_json_is_not_list():
    """Тест: JSON — объект, а не массив → вернуть пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = load_transactions("object.json")
        assert result == []


def test_io_error_during_file_opening():
    """Тест: ошибка IO при открытии файла → вернуть пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=IOError("File error")):
        result = load_transactions("error.json")
        assert result == []


def test_json_decode_error():
    """Тест: некорректный JSON → вернуть пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="malformed json")):
        result = load_transactions("malformed.json")
        assert result == []


def test_process_transaction_rub_success():
    """Тест: транзакция в RUB → вернуть сумму без изменений (успех)."""
    with patch("src.utils.convert_to_rub") as mock_convert:
        mock_convert.return_value = 1000.0

        transaction = {"operationAmount": {"amount": 1000, "currency": {"code": "RUB"}}}

        result = process_transaction(transaction)

        assert result == 1000.0
        mock_convert.assert_called_once_with({"amount": 1000, "currency": "RUB"})


def test_process_transaction_usd_success():
    """Тест: транзакция в USD → вызов конвертации (успех)."""
    with patch("src.utils.convert_to_rub") as mock_convert:
        mock_convert.return_value = 95000.0  # 100 USD ≈ 95 000 RUB

        transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}

        result = process_transaction(transaction)

        assert result == 95000.0
        mock_convert.assert_called_once_with({"amount": 100, "currency": "USD"})


def test_missing_operation_amount():
    """Тест: отсутствует 'operationAmount' → ValueError."""
    transaction = {"amount": 1000, "currency": "RUB"}

    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)

    assert "Транзакция должна содержать поле 'operationAmount'" in str(exc_info.value)


def test_missing_amount_in_operation_amount():
    """Тест: отсутствует 'amount' в 'operationAmount' → ValueError."""
    transaction = {"operationAmount": {"currency": {"code": "RUB"}}}

    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)

    assert "Транзакция должна содержать поле 'amount' в operationAmount" in str(exc_info.value)


def test_missing_currency_in_operation_amount():
    """Тест: отсутствует 'currency' в 'operationAmount' → ValueError."""
    transaction = {"operationAmount": {"amount": 1000}}

    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)

    assert "Транзакция должна содержать поле 'currency' в operationAmount" in str(exc_info.value)


def test_missing_code_in_currency():
    """Тест: отсутствует 'code' в 'currency' → ValueError."""
    transaction = {"operationAmount": {"amount": 1000, "currency": {}}}

    with pytest.raises(ValueError) as exc_info:
        process_transaction(transaction)

    assert "Поле 'currency' должно содержать ключ 'code'" in str(exc_info.value)
