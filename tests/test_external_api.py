import pytest
from unittest.mock import patch, Mock
import requests
from src.external_api import get_exchange_rate

def test_successful_usd_rate():
    """Тест: успешный запрос курса USD → вернуть курс из API."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {'rates': {'USD': 75.5}}

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('USD')
        assert result == 75.5

def test_successful_eur_rate():
    """Тест: успешный запрос курса EUR → вернуть курс из API."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {'rates': {'EUR': 82.3}}

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('EUR')
        assert result == 82.3

def test_network_error():
    """Тест: ошибка сети (RequestException) → вернуть 1.0."""
    with patch('requests.get', side_effect=requests.exceptions.RequestException('Network error')):
        result = get_exchange_rate('USD')
        assert result == 1.0

def test_api_http_error():
    """Тест: HTTP‑ошибка от API → вернуть 1.0."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('404 Not Found')

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('USD')
        assert result == 1.0

def test_missing_currency_in_response():
    """Тест: валюта отсутствует в ответе API (KeyError) → вернуть 1.0."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {'rates': {}}

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('JPY')
        assert result == 1.0


def test_empty_rates_in_response():
    """Тест: поле 'rates' отсутствует в ответе → вернуть 1.0."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {}

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('USD')
        assert result == 1.0


def test_large_currency_code():
    """Тест: длинный код валюты → корректно обработать или вернуть 1.0 при ошибке."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {'rates': {'VERY_LONG_CODE': 100.0}}

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('VERY_LONG_CODE')
        assert result == 100.0

def test_zero_rate():
    """Тест: курс равен 0 → вернуть 0.0."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {'rates': {'USD': 0.0}}

    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate('USD')
        assert result == 0.0