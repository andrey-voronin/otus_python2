from unittest import TestCase
import itertools

from lotto import Bag
from lotto import Card


class LottoTestCase(TestCase):
    def test_bag_values(self):
        bag = Bag(1, 10)
        self.assertEqual(len(bag), 10)
        self.assertEqual(max(bag.barrels), 10)
        self.assertEqual(min(bag.barrels), 1)

    def test_bag_get_barrel(self):
        bag = Bag(1, 5)
        self.assertEqual(len(bag), 5)
        bag.get_barrel()
        self.assertEqual(len(bag), 4)

    def test_card_values(self):
        card = Card(1, 99)
        self.assertEqual(len(card.numbers_array), card.card_row_n)
        for i in range(card.card_row_n):
            self.assertEqual(len(card.numbers_array[i]), card.card_col_n)
            numbers_row = list(filter(lambda x: x is not None, card.numbers_array[i]))
            self.assertEqual(len(numbers_row), card.card_value_n)

    def test_card_min_max(self):
        card = Card(1, 99)
        flattened_numbers = list(filter(lambda x: x is not None, itertools.chain(*card.numbers_array)))
        self.assertLessEqual(max(flattened_numbers), 99)
        self.assertGreaterEqual(min(flattened_numbers), 1)

    def test_card_all_numbers_different(self):
        card = Card(1, 99)
        different_flattened_numbers = set(filter(lambda x: x is not None, itertools.chain(*card.numbers_array)))
        self.assertEqual(len(different_flattened_numbers), card.card_value_n * card.card_row_n)

    def test_card_cross_out(self):
        card = Card(1, 99)
        one_number_col, one_number_from_card = \
        list(filter(lambda x: x[1] is not None, enumerate(card.numbers_array[0])))[0]
        card.cross_out(one_number_from_card)
        self.assertEqual(card.numbers_array[0][one_number_col], '--')
