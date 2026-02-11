def count_words(sentence: str) -> int:
    if not sentence:
        return 0
    return len(sentence.split())

def find_unique(lst):
    return [x for x in lst if lst.count(x) == 1]

def is_palindrome(s):
    s_str = str(s)
    return s_str == s_str[::-1]

def are_anagrams(str1, str2):
    return sorted(str1.replace(" ", "").lower()) == sorted(str2.replace(" ", "").lower())

def combine_dicts(d1, d2):
    combined = d1.copy()
    combined.update(d2)
    return combined
