def flat_list(lst):
    i = 0
    while i < len(lst):
        if isinstance(lst[i], list):
            flat_list(lst[i])
            lst[i:i+1] = lst[i]
        else:
            i += 1


list_a= [1, 2, 3, [4], 5, [6, [7, [], 8, [9]]]]
flat_list(list_a)
print(list_a)