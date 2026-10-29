import random

words = {
    "python": "A popular programming language",
    "computer": "An electronic machine",
    "college": "A place to study",
    "cricket": "A game played with bat and ball",
    "mobile": "A device used for calling",
    "keyboard": "Used for typing",
    "internet": "A global network"
}

score = 0
rounds = 5
attempts = 3

print("Welcome to Word Jumble Game!")

for i in range(rounds):
    word, hint = random.choice(list(words.items()))
    letters = list(word)
    random.shuffle(letters)
    jumble = "".join(letters)

    print("\nRound", i + 1)
    print("Scrambled word:", jumble)
    print("Hint:", hint)

    for j in range(attempts):
        guess = input("Guess the word: ").lower()

        if guess == word:
            print("Correct answer!")
            score += 10
            break
        else:
            print("Wrong answer!")
            print("Attempts left:", attempts - j - 1)
    else:
        print("Correct word was:", word)

    print("Current score:", score)
    words.pop(word)

print("\nGame Over!")
print("Your final score:", score, "out of", rounds * 10)
