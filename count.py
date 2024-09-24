#!/bin/env python3
"""
Подсчёт корейских слов в выгруженных карточках Anki.

1. Выгрузи карточки из Anki в текстовом формате.

2. Запусти скрипт`count.py deck1.txt dec2.txt ...

Скрипт выведет, сколько в каточках найдено различных слов с учётом морфологии.
"""

from collections import Counter
import sys
import re
from typing import Iterable, List
from konlpy.tag import Hannanum


def read_decks(file_names: Iterable[List[str]]) -> str:
    "Читает строки из файлов и объединяет в один текст."
    lines = []
    for file_name in file_names:
        with open(file_name, encoding="utf-8") as source:
            lines.extend(source.readlines())

    return "".join(lines)


NON_HANGEUL_RE = re.compile('[^ ㄱ-힣]+')


def strip_non_hangeul(text: str) -> str:
    "Возвращает текст, в котором все не-хангыльные символы заменены пробелами."
    return NON_HANGEUL_RE.sub(" ", text)


def count_stems(text: str) -> Counter[str]:
    "Возвращает объект Counter с подсчётом того, сколько раз каждый корень встретился в тексте."
    clean_text = strip_non_hangeul(text)
    h = Hannanum()
    tagged = h.pos(clean_text)
    # print(tagged)
    # tags = sorted(set(tag for _, tag in tagged))
    # for t in tags:
    #     print(t)
    #     print(sorted(set(word for word, tag in tagged if tag == t)))
    # print(sorted(set(tag for _, tag in tagged)))

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


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("\n".join((
            "Подсчёт корейских слов в выгруженных карточках Anki.",
            "",
            f"{sys.argv[0]} FILE ...",
            "")), file=sys.stderr)

    stems = count_stems(read_decks(sys.argv[1:]))
    print(sorted(stems))
    print(len(stems))
