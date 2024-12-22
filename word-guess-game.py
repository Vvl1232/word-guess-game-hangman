import random as rd
import streamlit as st

# Function to initialize or reset the game
def initialize_game():
    st.session_state.word = rd.choice(word_list)
    st.session_state.word_len = len(st.session_state.word)
    st.session_state.place_holder = ["_"] * st.session_state.word_len
    revealed_indices = rd.sample(range(st.session_state.word_len), k=max(3, st.session_state.word_len // 4))

    # Reveal some letters in the placeholder
    for index in revealed_indices:
        st.session_state.place_holder[index] = st.session_state.word[index]

    st.session_state.correct_list = []
    st.session_state.lives = 4
    st.session_state.consecutive_wrong_guesses = 0

# List of words
word_list = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
    "tiger", "zebra", "lemur", "otter", "sloth", "whale", "swine", "camel", "gecko", "koala",
    "hyena", "skunk", "midge", "quail", "viper", "finch", "llama", "moira", "mouse", "raven",
    "delhi", "paris", "cairo", "milan", "osaka", "perth", "quito", "tokyo", "dhaka", "seoul",
    "doha", "rabat", "sanaa", "tunis", "malmo", "nicos", "goaul", "omaha", "manta", "suva",
    "chess", "ludo", "poker", "darts", "check", "dices", "quizs", "mario", "bingo", "kites",
    "rummy", "jenga", "uno", "brawl", "magic", "blitz", "tetris", "slots", "carom", "revers"
]

# Initialize the game if it hasn't been done already
if 'word' not in st.session_state:
    initialize_game()

# Streamlit interface
st.title("🎉Hangman Word Guess Game🎉")
st.write(f"Word to guess: {' '.join(st.session_state.place_holder)}")
st.write(f"Lives remaining: {st.session_state.lives}")

# User input
guess = st.text_input("Enter guess letter:").lower()
submit = st.button("Submit Guess")
reset = st.button("Reset Game")

if submit and guess:
    if guess in st.session_state.word and guess not in st.session_state.correct_list:
        st.session_state.correct_list.append(guess)
        for i in range(st.session_state.word_len):
            if st.session_state.word[i] == guess:
                st.session_state.place_holder[i] = guess
        st.session_state.consecutive_wrong_guesses = 0
    elif guess not in st.session_state.correct_list:
        st.session_state.lives -= 1
        st.session_state.consecutive_wrong_guesses += 1
        st.warning(f"Incorrect guess! You have {st.session_state.lives} lives left.")
        
        if st.session_state.consecutive_wrong_guesses == 3:
            unrevealed_indices = [i for i in range(st.session_state.word_len) if st.session_state.place_holder[i] == "_"]
            if unrevealed_indices:
                index_to_reveal = rd.choice(unrevealed_indices)
                st.session_state.place_holder[index_to_reveal] = st.session_state.word[index_to_reveal]
                st.info(f"HINT:A letter has been revealed: {st.session_state.word[index_to_reveal]}")
            st.session_state.consecutive_wrong_guesses = 0

    st.write("Current word: " + " ".join(st.session_state.place_holder))

    if "_" not in st.session_state.place_holder:
        st.success(f"Congratulations! You've guessed the word: {st.session_state.word} 🎉")
    elif st.session_state.lives == 0:
        st.error(f"Game over! The word was: {st.session_state.word} 💀")

if reset:
    initialize_game()
