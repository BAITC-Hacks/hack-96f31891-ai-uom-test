#!/usr/bin/env python3
"""Терминальный FAQ-бот для репетиции HackAlem AI."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


FAQ_PATH = Path(__file__).with_name("faq.txt")
UNKNOWN_ANSWER = "Не знаю. Попробуйте спросить про время, команду, трек, сдачу или призы."
EXIT_WORDS = {"выход", "exit", "quit"}


@dataclass(frozen=True)
class FAQItem:
    question: str
    keywords: frozenset[str]
    answer: str


def normalize(text: str) -> set[str]:
    """Приводит строку к набору слов для простого сопоставления."""
    return set(re.findall(r"[а-яёa-z0-9]+", text.lower()))


def load_faq(path: Path = FAQ_PATH) -> list[FAQItem]:
    """Загружает пары вопрос–ответ из FAQ-файла."""
    items: list[FAQItem] = []
    for block in path.read_text(encoding="utf-8").strip().split("\n\n"):
        fields = {}
        for line in block.splitlines():
            label, value = line.split(":", maxsplit=1)
            fields[label.strip()] = value.strip()
        items.append(
            FAQItem(
                question=fields["Вопрос"],
                keywords=frozenset(normalize(fields["Ключевые слова"])),
                answer=fields["Ответ"],
            )
        )
    return items


def find_answer(user_question: str, items: Iterable[FAQItem]) -> Optional[str]:
    """Возвращает ответ с наибольшим числом совпавших ключевых слов."""
    words = normalize(user_question)
    best_item: Optional[FAQItem] = None
    best_score = 0

    for item in items:
        score = len(words & item.keywords)
        if score > best_score:
            best_item = item
            best_score = score

    return best_item.answer if best_item else None


def main() -> None:
    faq_items = load_faq()
    print("FAQ-бот репетиции HackAlem AI")
    print("Спросите про время, команду, трек, сдачу или призы.")
    print("Для выхода напишите: выход\n")

    while True:
        try:
            user_question = input("Вы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо встречи!")
            break

        if user_question.lower() in EXIT_WORDS:
            print("Бот: До встречи!")
            break
        if not user_question:
            print("Бот: Задайте вопрос, пожалуйста.")
            continue

        answer = find_answer(user_question, faq_items)
        print(f"Бот: {answer or UNKNOWN_ANSWER}")


if __name__ == "__main__":
    main()
