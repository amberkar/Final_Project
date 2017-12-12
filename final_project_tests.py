import unittest
from final_project_code import *

class Test_events_caching(unittest.TestCase):
  def setUp(self):
    self.cache_file = open("events_cache_contents.json", encoding='utf-8-sig')

  def test_events_cache_file(self):
    read = self.cache_file.read()
    self.assertTrue(read)
    self.assertIsInstance(read, str)
    cache_diction = json.loads(read)
    self.assertIsInstance(cache_diction, dict)

  def tearDown(self):
    self.cache_file.close()

class Test_formats_caching(unittest.TestCase):
  def setUp(self):
    self.cache_file = open("formats_cache_contents.json", encoding='utf-8-sig')

  def test_formats_cache_file(self):
    read = self.cache_file.read()
    self.assertTrue(read)
    self.assertIsInstance(read, str)
    cache_diction = json.loads(read)
    self.assertIsInstance(cache_diction, dict)

  def tearDown(self):
    self.cache_file.close()

class Test_categories_caching(unittest.TestCase):
  def setUp(self):
    self.cache_file = open("categories_cache_contents.json", encoding='utf-8-sig')

  def test_categories_cache_file(self):
    read = self.cache_file.read()
    self.assertTrue(read)
    self.assertIsInstance(read, str)
    cache_diction = json.loads(read)
    self.assertIsInstance(cache_diction, dict)

  def tearDown(self):
    self.cache_file.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
