import random
import streamlit as st

WORDS = {
    "python": "A popular programming language",
    "computer": "An electronic machine used to process data",
    "college": "A place where students study",
    "cricket": "A game played with a bat and ball",
    "keyboard": "An input device used to type",
    "internet": "A worldwide network of connected computers",
    "library": "A place where books are kept",
    "science": "The study of the natural world",
    "program": "A set of instructions given to a computer",
    "student": "A person who studies"
}

TOTAL_ROUNDS = 5
ATTEMPTS_PER_ROUND = 3
POINTS_PER_CORRECT_ANSWER = 10


def new_game():
    selected_words = random.sample(list(WORDS.keys()), TOTAL_ROUNDS)
    st.session_state.round_words = selected_words
    st.session_state.round_index = 0
    st.session_state.score = 0
    st.session_state.attempts_left = ATTEMPTS_PER_ROUND
    st.session_state.finished_rounds = []
    st.session_state.message = ""
    st.session_state.game_over = False
    st.session_state.scrambled_word = scramble_word(selected_words[0])


def scramble_word(word):
    letters = list(word)
    scrambled = word
    while scrambled == word and len(set(word)) > 1:
        random.shuffle(letters)
        scrambled = "".join(letters)
    return scrambled


def move_to_next_round():
    st.session_state.round_index += 1
    st.session_state.attempts_left = ATTEMPTS_PER_ROUND
    st.session_state.message = ""
    if st.session_state.round_index >= TOTAL_ROUNDS:
        st.session_state.game_over = True
    else:
        word = st.session_state.round_words[st.session_state.round_index]
        st.session_state.scrambled_word = scramble_word(word)


st.set_page_config(page_title="Word Jumble Game", page_icon="🔤", layout="centered")

st.title("🔤 Word Jumble Game")
st.write("Unscramble the letters, use the hint, and guess the correct word.")

if "round_words" not in st.session_state:
    new_game()

if st.session_state.game_over:
    st.success("Game completed!")
    st.subheader(f"Your final score: {st.session_state.score} / {TOTAL_ROUNDS * POINTS_PER_CORRECT_ANSWER}")
    st.write("Thanks for playing!")
    if st.button("Play Again", use_container_width=True):
        new_game()
        st.rerun()
else:
    index = st.session_state.round_index
    answer = st.session_state.round_words[index]
    st.progress(index / TOTAL_ROUNDS)
    st.caption(f"Round {index + 1} of {TOTAL_ROUNDS}")
    st.metric("Score", f"{st.session_state.score} / {TOTAL_ROUNDS * POINTS_PER_CORRECT_ANSWER}")
    st.metric("Attempts left", st.session_state.attempts_left)

    st.markdown("### Unscramble this word")
    st.markdown(f"<h2 style='text-align:center; letter-spacing:5px'>{st.session_state.scrambled_word.upper()}</h2>", unsafe_allow_html=True)
    st.info(f"Hint: {WORDS[answer]}")

    with st.form(key=f"guess_form_{index}_{ATTEMPTS_PER_ROUND - st.session_state.attempts_left}"):
        guess = st.text_input("Your answer", placeholder="Type the correct word").strip().lower()
        submitted = st.form_submit_button("Submit Answer", use_container_width=True)

    if submitted:
        if not guess:
            st.warning("Please enter a word.")
        elif guess == answer:
            st.session_state.score += POINTS_PER_CORRECT_ANSWER
            st.session_state.message = f"Correct! The word was '{answer}'. You earned {POINTS_PER_CORRECT_ANSWER} points."
            st.session_state.finished_rounds.append(answer)
            st.success(st.session_state.message)
            st.session_state.round_index += 1
            st.session_state.attempts_left = ATTEMPTS_PER_ROUND
            if st.session_state.round_index >= TOTAL_ROUNDS:
                st.session_state.game_over = True
            else:
                next_word = st.session_state.round_words[st.session_state.round_index]
                st.session_state.scrambled_word = scramble_word(next_word)
            st.rerun()
        else:
            st.session_state.attempts_left -= 1
            if st.session_state.attempts_left <= 0:
                st.warning(f"No attempts left. The correct word was '{answer}'.")
                st.session_state.finished_rounds.append(answer)
                move_to_next_round()
                st.rerun()
            else:
                st.error(f"Incorrect answer. Try again! Attempts left: {st.session_state.attempts_left}")

    st.caption("Correct answer = +10 points. You get 3 attempts in each round.")
