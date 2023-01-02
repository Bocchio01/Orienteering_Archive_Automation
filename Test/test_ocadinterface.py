import unittest

from Utils.ocadinterface import *

# get_query(ocdFile=BASE_FILE_PATH, filter=OCADFilter.MAPNOTES.value)


class TestGetQuery(unittest.TestCase):
    def test_valid_input(self):
        # Test with valid input
        result = get_query(
            r"C:\Users\Bocchio\Documents\MEGAsync\Orienteering\Carte\Casa\Casa 400.ocd", 0)
        self.assertIsNotNone(result)

    def test_invalid_path(self):
        # Test with invalid path
        with self.assertRaises(FileNotFoundError):
            get_query('/invalid/path/to/ocd/file.ocd', 0)

    def test_dict_query(self):
        # Test with dict query
        query = {0: 'value1', 1: 'value2'}
        result = get_query(query, 0)
        self.assertEqual(result, 'value1')

    def test_list_query(self):
        # Test with list query
        query = ['value1', 'value2']
        result = get_query(query, 1)
        self.assertEqual(result, 'value2')

    def test_index_out_of_range(self):
        # Test with index out of range
        query = ['value1', 'value2']
        result = get_query(query, 2)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
