def merge_sorted_list(list1, list2):
    i, j = 0, 0
    merged = []

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1

    while i < len(list1):
        merged.append(list1[i])
        i += 1

    while j < len(list2):
        merged.append(list2[j])
        j += 1

    return merged

a = [1, 3, 5, 7]
b = [2, 4, 6, 8, 10]

print(merge_sorted_list(a, b))