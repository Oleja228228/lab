def count_digits(s):
    count = 0
    for ch in s:
        if ch.isdigit():
            count += 1
    return count