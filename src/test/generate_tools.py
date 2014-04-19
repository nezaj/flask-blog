"""
Tools for generating random test data.
"""

import random
from collections import namedtuple

from test.dummy import words

PostStruct = namedtuple('PostStruct', ["author", "title", "content", "tags", "draft"])

def random_range(a, b):
    "Returns a range from 0 to a random integer."
    return range(random.randint(a, b))

def generate_phrase(min_words=3, max_words=5):
    "Generates a phrase with words chosen at random without replacement"
    num_words = len(random_range(min_words, max_words))
    return " ".join(random.sample(words, num_words))

def generate_content(min_phrases=3, max_phrases=5):
    " Generates content based on random sentences "
    return " ".join(generate_phrase() for _ in random_range(min_phrases, max_phrases))

def generate_tags():
    " Generates a random list of tags "
    return generate_phrase().split()

def generate_post(author="nezaj", title=None):
    if title is None:
        title = generate_phrase(min_words=1, max_words=2)
    return PostStruct(author=author, title=title, content=generate_content(), tags=generate_tags(), draft=False)
