import pytest
from functions import count_words, find_unique, is_palindrome, are_anagrams, combine_dicts

def test_count_words():
    assert count_words("Hello world") == 2
    assert count_words("") == 0
    assert count_words("One two three four") == 4
    assert count_words("   multiple   spaces ") == 2
    assert count_words("Hello world") == 3

def test_find_unique():
    assert find_unique([1, 2, 2, 3, 4, 4, 5]) == [1, 3, 5]
    assert find_unique(["a", "b", "a"]) == ["b"]
    assert find_unique([]) == []

def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("12321") is True
    assert is_palindrome("hello") is False
    assert is_palindrome(1221) is True

def test_are_anagrams():
    assert are_anagrams("listen", "silent") is True
    assert are_anagrams("triangle", "integral") is True
    assert are_anagrams("hello", "billion") is False
    assert are_anagrams("Dormitory", "Dirty room") is True  

def test_combine_dicts():
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    result = combine_dicts(d1, d2)
    assert result == {"a": 1, "b": 3, "c": 4}
    assert combine_dicts({}, {"x": 10}) == {"x": 10}
    assert combine_dicts({"y": 5}, {}) == {"y": 5}
