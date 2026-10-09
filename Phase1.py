import random

words = {
    "python": "A popular programming language",
    "computer": "An electronic machine"
}

score = 0
rounds = 5
attempts = 3

print("Welcome to Word Jumble Game!")

word, hint = random.choice(list(words.items()))
letters = list(word)
random.shuffle(letters)
jumble = "".join(letters)

print("Scrambled word:", jumble)
print("Hint:", hint)
