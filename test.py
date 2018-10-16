from spider import Scheduler
import unittest

class TestSche(unittest.TestCase):
    def test_get(self):
        sche=Scheduler()
        sche.add_url('abc')
        self.assertEqual(sche.get_url(),'abc')
        self.assertEqual(sche.get_url(),None)

if __name__ == '__main__':
    unittest.main()
