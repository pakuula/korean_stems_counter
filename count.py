#!/bin/env python3
"""
Подсчёт корейских слов в выгруженных карточках Anki.

1. Выгрузи карточки из Anki в текстовом формате.

2. Запусти скрипт`count.py deck1.txt dec2.txt ...

Скрипт выведет, сколько в каточках найдено различных слов с учётом морфологии.

Вообще говоря, скрипт работает с любыми текстовыми файлами
и выводит список корней встреченных корейских слов.
"""

from collections import Counter
import sys
import re
from typing import Iterable, List
from konlpy.tag import Hannanum, Mecab

TAGS = {
    "VV": "Verb",
    "VX": "Auxiliary Verb",
    "VA": "형용사: adjective",
    "NNG": "General noun",
    "NNP": "고유명사: proper noun, proper name",
    "NR": "numeral",
    "NP": "대명사: pronoun",
    "NNB": "bound noun",
    "NNBC": "bound noun (counting nouns?)",
    "MAJ": "Conjunctive adverb MAJ",
    "MAG": "General Adverb",
    "MM": "Adjective",
    "XR": "어근: root",
}

TRANSFORMER = {
    "VV": lambda word: word + "다",
    "VX": lambda word: word + "다",
    "VA": lambda word: word + "다",
    "XR": lambda word: word + "하다",
}


def read_decks(file_names: Iterable[List[str]]) -> str:
    "Читает строки из файлов и объединяет в один текст."
    lines = []
    for file_name in file_names:
        with open(file_name, encoding="utf-8") as source:
            lines.extend(source.readlines())

    return "".join(lines)


NON_HANGEUL_RE = re.compile('[^.,; ㄱ-힣]+')


def strip_non_hangeul(text: str) -> str:
    "Возвращает текст, в котором все не-хангыльные символы заменены пробелами."
    return NON_HANGEUL_RE.sub(" ", text)


def count_stems_hannanum(text: str) -> Counter[str]:
    "Возвращает объект Counter с подсчётом того, сколько раз каждый корень встретился в тексте."
    clean_text = strip_non_hangeul(text)
    h = Hannanum()
    tagged = h.pos(clean_text)

    # M - непонятно что
    # N - существительные
    # P - глаголы и прилагательные
    counter = Counter()
    for word, tag in tagged:
        if tag in "MNP":
            if tag == "P":
                word += "다"  # verb
            counter[word] += 1
    return counter


def count_stems_mecab(text: str) -> Counter[str]:
    "Возвращает объект Counter с подсчётом того, сколько раз каждый корень встретился в тексте."
    clean_text = strip_non_hangeul(text)
    tagger = Mecab()
    tagged = tagger.pos(clean_text)
    counter = Counter()
    for word, tag in tagged:
        if tag in TAGS:
            if tag in TRANSFORMER:
                word = TRANSFORMER[tag](word)
            counter[word] += 1
    return counter


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("\n".join((
            "Подсчёт корейских слов в выгруженных карточках Anki.",
            "",
            f"{sys.argv[0]} FILE ...",
            "")), file=sys.stderr)

    # stems = count_stems_hannanum(read_decks(sys.argv[1:]))
    # print(sorted(stems))
    # print(len(stems))
    stems = count_stems_mecab(read_decks(sys.argv[1:]))
    print(sorted(stems))
    print(len(stems))
