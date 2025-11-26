word1 = input("Write first word: ").lower()
word2 = input("Write second word: ").lower()

symbol1 = list(word1)
symbol2 = list(word2)

if sorted(symbol1) == sorted(symbol2):
    print("True")
else:
    print("False")

