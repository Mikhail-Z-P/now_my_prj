from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import API_KEY, convert_to_rub


def test_usd_to_rub_conversion():
    """Тест успешной конвертации USD → RUB через API."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 9500.0}
        mock_get.return_value = mock_response

        transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}

        result = convert_to_rub(transaction)

        assert result == 9500.0
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]
        assert call_args["params"]["from"] == "USD"
        assert call_args["params"]["to"] == "RUB"
        assert call_args["params"]["amount"] == 100
        assert call_args["headers"]["apikey"] == API_KEY


def test_eur_to_rub_conversion():
    """Тест успешной конвертации EUR → RUB через API."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 8800.0}
        mock_get.return_value = mock_response

        transaction = {"operationAmount": {"amount": 80, "currency": {"code": "EUR"}}}

        result = convert_to_rub(transaction)

        assert result == 8800.0
        mock_get.assert_called_once()


def test_rub_transaction_no_conversion():
    """Тест транзакции в RUB — конвертация не требуется."""
    with patch("src.external_api.requests.get") as mock_get:
        transaction = {"operationAmount": {"amount": 5000, "currency": {"code": "RUB"}}}

        result = convert_to_rub(transaction)

        assert result == 5000.0
        mock_get.assert_not_called()


def test_fractional_amount_conversion():
    """Тест конвертации с дробной суммой."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 2422.5}
        mock_get.return_value = mock_response

        transaction = {"operationAmount": {"amount": 25.5, "currency": {"code": "USD"}}}

        result = convert_to_rub(transaction)

        assert result == 2422.5
        mock_get.assert_called_once()


def test_unsupported_currency():
    """Тест с неподдерживаемой валютой (JPY)."""
    transaction = {"operationAmount": {"amount": 10000, "currency": {"code": "JPY"}}}

    with pytest.raises(ValueError) as exc_info:
        convert_to_rub(transaction)

    assert "Неподдерживаемая валюта: JPY" in str(exc_info.value)


def test_missing_operation_amount():
    """Тест: отсутствует поле 'operationAmount'."""
    transaction = {"amount": 1000, "currency": "USD"}

    with pytest.raises(KeyError) as exc_info:
        convert_to_rub(transaction)

    assert "'operationAmount'" in str(exc_info.value)


def test_missing_amount_in_operation_amount():
    """Тест: отсутствует 'amount' в 'operationAmount'."""
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}

    with pytest.raises(KeyError) as exc_info:
        convert_to_rub(transaction)

    assert "'amount'" in str(exc_info.value)


def test_missing_currency_in_operation_amount():
    """Тест: отсутствует 'currency' в 'operationAmount'."""
    transaction = {"operationAmount": {"amount": 100}}

    with pytest.raises(KeyError) as exc_info:
        convert_to_rub(transaction)

    assert "'currency'" in str(exc_info.value)


def test_missing_code_in_currency():
    """Тест: отсутствует 'code' в 'currency'."""
    transaction = {"operationAmount": {"amount": 100, "currency": {}}}

    with pytest.raises(KeyError) as exc_info:
        convert_to_rub(transaction)

    assert "'code'" in str(exc_info.value)


def test_non_numeric_amount():
    """Тест: 'amount' не является числом."""
    transaction = {"operationAmount": {"amount": "не число", "currency": {"code": "USD"}}}

    with pytest.raises(ValueError) as exc_info:
        convert_to_rub(transaction)

    assert "could not convert string to float" in str(exc_info.value)


def test_api_error_404():
    """Тест: ошибка API (404 Not Found)."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            convert_to_rub(transaction)

        assert "404 Client Error" in str(exc_info.value)
        mock_get.assert_called_once()


def test_api_timeout():
    """Тест: таймаут API-запроса."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}

        with pytest.raises(requests.exceptions.Timeout) as exc_info:
            convert_to_rub(transaction)

        assert "Request timed out" in str(exc_info.value)
