import unittest
import quandl
from store_data import get_stock_data

API_FILE = "api_key.txt"

class Testing(unittest.TestCase):
    """Simple test cases for API retrieval"""

    def test_wrong_input(self):
        """
        Test to make sure wrong inputs can't be fed
        into the function
        """
        test1 = False
        test2 = False

        try:
            get_stock_data(None)
        except AssertionError:
            test1 = True

        try:
            get_stock_data(55)
        except AssertionError:
            test2 = True

        self.assertTrue(test1)
        self.assertTrue(test2)

    def test_getting_data(self):
        """Test that data is returned"""

        gme = get_stock_data("GME")
        self.assertFalse(gme.empty)

        multiple = get_stock_data(["NOK", "GME", "AMC"])
        self.assertFalse(multiple.empty)

        erroneous = get_stock_data(";laksdj;flkasjd;a")
        self.assertTrue(erroneous.empty)

if __name__ == '__main__':
    # Set quandl api key
    quandl.read_key(filename=API_FILE)

    unittest.main()
