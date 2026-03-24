from unittest.mock import patch, Mock
from external_api import convert_to_rub

def test_usd_conversion_success():
    """Тест успешной конвертации USD → RUB через API"""
    with patch('external_api.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 9500.0}
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)

        assert result == 9500.0, f"Ожидалось 9500.0, получено {result}"
        mock_get.assert_called_once()

def test_eur_conversion_success():
    """Тест успешной конвертации EUR → RUB через API"""
    with patch('external_api.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 10500.0}
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "EUR"}
        result = convert_to_rub(transaction)

        assert result == 10500.0, f"Ожидалось 10500.0, получено {result}"

def test_rub_currency_no_conversion():
    """Тест для валюты RUB — конвертация не нужна"""
    transaction = {"amount": 5000, "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 5000.0, f"Ожидалось 5000.0, получено {result}"

def test_unsupported_currency():
    """Тест для неподдерживаемой валюты"""
    transaction = {"amount": 100, "currency": "JPY"}
    try:
        convert_to_rub(transaction)
        assert False, "Ожидалась ошибка ValueError"
    except ValueError as e:
        assert "Неподдерживаемая валюта" in str(e), f"Неверный текст ошибки: {e}"

def test_api_unauthorized_401():
    """Тест обработки ошибки 401 Unauthorized"""
    with patch('external_api.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)
        assert result == 100.0, f"Ожидалось 100.0, получено {result}"

def test_api_network_error():
    """Тест обработки сетевой ошибки"""
    with patch('external_api.requests.get', side_effect=Exception("Network error")):
        transaction = {"amount": 200, "currency": "EUR"}
        result = convert_to_rub(transaction)
        assert result == 200.0, f"Ожидалось 200.0, получено {result}"

def test_api_missing_result_field():
    """Тест обработки ответа API без поля 'result'"""
    with patch('external_api.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rate": 90.0}
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)
        assert result == 100.0, f"Ожидалось 100.0, получено {result}"

def test_invalid_transaction_structure():
    """Тест с некорректной структурой транзакции"""
    # Отсутствует поле 'currency'
    transaction1 = {"amount": 100}
    try:
        convert_to_rub(transaction1)
        assert False, "Ожидалась KeyError при отсутствии 'currency'"
    except KeyError:
        pass

    transaction2 = {"currency": "USD"}
    try:
        convert_to_rub(transaction2)
        assert False, "Ожидалась KeyError при отсутствии 'amount'"
    except KeyError:
        pass