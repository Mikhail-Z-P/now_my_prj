import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "fixture,state",
    [
        ("trans_default", None),
        ("trans_custom", "PENDING"),
        ("empty_trans", None),
        ("trans_no_match", "EXECUTED"),
        ("trans_missing_key", None),
    ],
)
def test_filter_by_state(fixture, state, request):
    transactions, expected = request.getfixturevalue(fixture)
    result = filter_by_state(transactions, state=state) if state else filter_by_state(transactions)
    assert result == expected


# def test_default(trans_default):
#     """Проверяет базовую фильтрацию транзакций."""
#     transactions, expected = trans_default
#     assert filter_by_state(transactions) == expected
#
#
# def test_custom(trans_custom):
#     """Тестирует фильтрацию с кастомным состоянием ('PENDING')."""
#     transactions, expected = trans_custom
#     assert filter_by_state(transactions, state="PENDING") == expected
#
#
# def test_empty(empty_trans):
#     """Проверяет обработку пустых транзакций."""
#     transactions, expected = empty_trans
#     assert filter_by_state(transactions) == expected
#
#
# def test_no_match(trans_no_match):
#     """Тестирует случай, когда ни одна транзакция не соответствует фильтру ('EXECUTED')."""
#     transactions, expected = trans_no_match
#     assert filter_by_state(transactions, state="EXECUTED") == expected
#
#
# def test_missing_key(trans_missing_key):
#     """Проверяет обработку транзакций без ключа 'state'."""
#     transactions, expected = trans_missing_key
#     assert filter_by_state(transactions) == expected


def test_all_match(trans_all_match):
    """Тестирует случай, когда все транзакции соответствуют фильтру."""
    transactions, expected = trans_all_match
    assert filter_by_state(transactions) == expected


def test_case_sensitive(trans_case_sensitive):
    """Проверяет чувствительность фильтра к регистру ('EXECUTED')."""
    transactions, expected = trans_case_sensitive
    assert filter_by_state(transactions, state="EXECUTED") == expected


def test_non_string(trans_non_string):
    """Тестирует передачу нестрокового значения для state (например, 1)."""
    transactions, expected = trans_non_string
    assert filter_by_state(transactions, state=1) == expected


def test_asc(data_asc):
    """Проверяет сортировку транзакций по дате (возрастание)."""
    inp, exp = data_asc
    assert sort_by_date(inp, sorting=True) == exp


def test_desc(data_desc):
    """Проверяет сортировку транзакций по дате (убывание)."""
    inp, exp = data_desc
    assert sort_by_date(inp, sorting=False) == exp


def test_single(single):
    """Тестирует сортировку одной транзакции."""
    inp, exp = single
    assert sort_by_date(inp) == exp


def test_missing(missing_date):
    """Проверяет обработку транзакций с отсутствующей датой."""
    inp, exp = missing_date
    assert sort_by_date(inp, sorting=True) == exp


def test_same(same_dates):
    """Тестирует сортировку транзакций с одинаковыми датами."""
    inp, exp = same_dates
    assert sort_by_date(inp, sorting=True) == exp


def test_iso(iso_dates):
    """Проверяет сортировку дат в формате ISO."""
    inp, exp = iso_dates
    assert sort_by_date(inp, sorting=True) == exp


def test_orig(orig):
    """Убеждается, что исходные данные не изменены после сортировки."""
    orig_copy = orig.copy()
    sort_by_date(orig_copy, sorting=True)
    assert orig_copy == orig


def test_num(num_dates):
    """Тестирует сортировку числовых дат."""
    inp, exp = num_dates
    assert sort_by_date(inp, sorting=True) == exp


def test_mixed(mixed):
    """Проверяет выброс исключения TypeError при смешивании несовместимых типов дат."""
    with pytest.raises(TypeError):
        sort_by_date(mixed, sorting=True)
