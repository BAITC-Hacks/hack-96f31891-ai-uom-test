import unittest

from main import UNKNOWN_ANSWER, find_answer, load_faq


class FAQBotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = load_faq()

    def test_has_five_faq_items(self):
        self.assertEqual(len(self.items), 5)

    def test_finds_submission_answer(self):
        answer = find_answer("Когда дедлайн сдачи репозитория?", self.items)
        self.assertIn("22 сентября 20:00", answer)

    def test_returns_none_for_unknown_question(self):
        self.assertIsNone(find_answer("Какая сегодня погода?", self.items))
        self.assertTrue(UNKNOWN_ANSWER.startswith("Не знаю"))
