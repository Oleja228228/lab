def unique_elements(nested_list):
    unique = set()

    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                flatten(item)
            else:
                unique.add(item)

    flatten(nested_list)
    return list(unique)

list_a = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2 ,3]]]]
print(unique_elements(list_a))
