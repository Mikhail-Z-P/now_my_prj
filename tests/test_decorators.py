import pytest

from src.decorators import log


def test_successful_console(capsys):
    """Успешное выполнение — консоль."""

    @log()
    def add(a, b):
        return a + b

    result = add(3, 5)
    captured = capsys.readouterr()
    output_lines = [line.strip() for line in captured.out.strip().split("\n") if line.strip()]

    assert result == 8
    assert len(output_lines) == 2
    assert output_lines[0] == "add start. Inputs: (3, 5)"
    assert output_lines[1] == "add ok"


def test_error_console(capsys):
    """Ошибка — консоль."""

    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    output_lines = [line.strip() for line in captured.out.strip().split("\n") if line.strip()]

    assert len(output_lines) == 2
    assert output_lines[0] == "divide start. Inputs: (10, 0)"
    assert output_lines[1].startswith("divide error: ZeroDivisionError. Inputs: (10, 0)")


def test_kwargs_console(capsys):
    """Ключевые аргументы — консоль."""

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    captured = capsys.readouterr()
    output_lines = [line.strip() for line in captured.out.strip().split("\n") if line.strip()]

    assert result == "Hi, Alice!"
    assert output_lines[0] == "greet start. Inputs: ('Alice', greeting='Hi')"
    assert output_lines[1] == "greet ok"


def test_successful_file(tmp_path):
    """Успешное выполнение — файл."""
    log_file = tmp_path / "test.txt"

    @log(filename=str(log_file))
    def mul(a, b):
        return a * b

    result = mul(4, 6)
    assert result == 24

    with open(log_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 2
    assert lines[0] == "mul start. Inputs: (4, 6)"
    assert lines[1] == "mul ok"


def test_no_args_console(capsys):
    """Без аргументов — консоль."""

    @log()
    def pi():
        return 3.14

    result = pi()
    captured = capsys.readouterr()
    output_lines = [line.strip() for line in captured.out.strip().split("\n") if line.strip()]

    assert abs(result - 3.14) < 1e-5
    assert output_lines[0] == "pi start. Inputs: ()"
    assert output_lines[1] == "pi ok"
