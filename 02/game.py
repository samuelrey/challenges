#!python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

from data import DICTIONARY, LETTER_SCORES, POUCH
import itertools
import random

NUM_LETTERS = 7


# re-use from challenge 01
def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


# re-use from challenge 01
def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)


def draw_letters():
    return random.sample(POUCH, NUM_LETTERS)


def get_possible_dict_words(draw):
    out = []
    perm = _get_permutations_draw(draw)
    for word in perm:
        word = ''.join(word).lower()
        if word in DICTIONARY:
            out.append(word)
    return out


def _get_permutations_draw(draw):
    return itertools.chain.from_iterable(
        list(
            itertools.permutations(draw, n) for n in range(1, NUM_LETTERS + 1)
            )
        )


def _validation(word, draw):
    letters = list(draw)
    for ch in word.upper():
        if ch in letters:
            letters.remove(ch)
        else:
            raise ValueError('{} is not a valid word!'.format(word))
    if not word.lower() in DICTIONARY:
        raise ValueError('{} is not in the dictionary!'.format(word))
    return word


def input_word(draw):
    while True:
        try:
            word = raw_input('Form a valid word: ')
            _validation(word, draw)
            return word
        except ValueError as e:
            print e
            pass


def main():
    drawn = draw_letters()
    print 'Letters drawn: ' + str(drawn)

    user_word = input_word(drawn)
    user_value = calc_word_value(user_word)
    print 'Word chosen: {} (Value: {})'.format(user_word, user_value)

    possible_words = get_possible_dict_words(drawn)
    max_word = max_word_value(possible_words)
    max_value = calc_word_value(max_word)
    print 'Optimal word: {} (Value: {})'.format(max_word, max_value)

    score = float(user_value) / max_value * 100.0
    print 'You scored: {:.1f}'.format(score)


if __name__ == "__main__":
    main()
