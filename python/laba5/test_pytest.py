import pytest
from test import count_digits

def test_empty_string():
    assert count_digits("") == 0

def test_no_digits():
    assert count_digits("abcdef") == 0

def test_only_digits():
    assert count_digits("12345") == 5

def test_mixed_string():
    assert count_digits("a1b2c3") == 3

def test_digits_and_symbols():
    assert count_digits("!@#123$%^") == 3

def test_spaces_and_digits():
    assert count_digits("1 2 3") == 3
def test_long_string():
    assert count_digits("a" * 1000 + "12345") == 5

def test_only_spaces():
    assert count_digits("     ") == 0

def test_newlines_and_tabs():
    assert count_digits("1\n2\t3") == 3

def test_negative_sign_like_text():
    assert count_digits("-123") == 3

def test_float_like_string():
    assert count_digits("3.14") == 3

def test_non_string_input():
    try:
        count_digits(12345)
        assert False
    except TypeError:
        assert True