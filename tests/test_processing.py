import pytest
import re
from processing import filter_by_state, sort_by_date

def test_filter_by_state_default():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"}
    ]
    result = filter_by_state(transactions)
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    assert result == expected

def test_filter_by_state_custom():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "FAILED"}
    ]
    result = filter_by_state(transactions, state="PENDING")
    expected = [{"id": 2, "state": "PENDING"}]
    assert result == expected


def test_filter_by_state_empty_list():
    result = filter_by_state([])
    assert result == []


def test_filter_by_state_no_matches():
    transactions = [
        {"id": 1, "state": "PENDING"},
        {"id": 2, "state": "FAILED"}
    ]
    result = filter_by_state(transactions, state="EXECUTED")
    assert result == []

def test_filter_by_state_missing_key():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "status": "PENDING"},
        {"id": 3, "state": "EXECUTED"}
    ]
    result = filter_by_state(transactions)
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    assert result == expected

def test_filter_by_state_all_matches():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    result = filter_by_state(transactions)
    assert result == transactions

def test_filter_by_state_case_sensitive():
    transactions = [
        {"id": 1, "state": "executed"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "Executed"}
    ]
    result = filter_by_state(transactions, state="EXECUTED")
    expected = [{"id": 2, "state": "EXECUTED"}]
    assert result == expected

def test_filter_by_state_non_string_state():
    transactions = [
        {"id": 1, "state": 1},
        {"id": 2, "state": 2}
    ]
    result = filter_by_state(transactions, state=1)
    expected = [{"id": 1, "state": 1}]
    assert result == expected


