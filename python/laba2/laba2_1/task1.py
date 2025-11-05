text = input("Write your text: ").lower()
word = text.split()

d = {}
for w in word:
    if w in d:
        d[w] += 1
    else:
        d[w] = 1

print(d)
print(len(d))