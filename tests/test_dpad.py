from unittest import TestCase
from xbox_wireless.core import DPad


class TestDPad(TestCase):
    def test_1(self):
        d = DPad(1)

        self.assertEqual(d.up, True)
        self.assertEqual(d.right, False)
        self.assertEqual(d.down, False)
        self.assertEqual(d.left, False)
