from django.test import TestCase

from .models import Lemma

class SortFormTest(TestCase):
    def test_sortform_equivalent_to_cf(self):
        lem = Lemma(
            cf="ŋšřḫ",
            sortform="gzszrzhz"
        )
        self.assertEqual(lem.sortform, lem.make_sortform())
