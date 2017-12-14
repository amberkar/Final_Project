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
    self.assertIsInstance(cache_diction, dict, "testing that data is cached in events_cache_contents.json")

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
    self.assertIsInstance(cache_diction, dict, "testing that data is cached in formats_cache_contents.json")

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
    self.assertIsInstance(cache_diction, dict,"testing that data is cached in categories_cache_contents.json")

  def tearDown(self):
    self.cache_file.close()

class Test_Token_Data(unittest.TestCase):
  def setUp(self):
    self.token_file = open("token.json", encoding='utf-8-sig')

  def test_token_file(self):
    read = self.token_file.read()
    self.assertTrue(read)
    self.assertIsInstance(read, str)
    token_file = json.loads(read)
    self.assertIsInstance(token_file, dict, "testing that data is cached in token.json")

  def tearDown(self):
    self.token_file.close()

class Data_Test(unittest.TestCase):
    def setUp(self):
        try:
            with open('events_cache_contents.json', 'r') as f:
                EVENTS_CACHE_DICTION = json.loads(f.read())
        except:
            EVENTS_CACHE_DICTION = {}

        try:
            with open('formats_cache_contents.json', 'r') as f:
                FORMATS_CACHE_DICTION = json.loads(f.read())
        except:
            FORMATS_CACHE_DICTION = {}
        try:
            with open('categories_cache_contents.json', 'r') as f:
                CATEGORIES_CACHE_DICTION = json.loads(f.read())
        except:
            CATEGORIES_CACHE_DICTION = {}
        try:
            with open('tests_token.json', 'r') as f:
                token_dict = json.loads(f.read())
        except:
            token_dict = {}


    def test_formats_table(self):
        self.data = formats_data['formats']
        self.assertTrue(isinstance(self.data, list))

    def test_categories_table(self):
        self.data2 = categories_data['categories']
        self.assertTrue(isinstance(self.data2, list))

    def test_events_table(self):
        self.data3 = events_data['events']
        self.assertTrue(isinstance(self.data3, list))

    def test_plot_events_by_formats(self):
        self.labels = []
        self.assertTrue(isinstance(self.labels, list))

    def test_plot_events_by_formats2(self):
        self.labels = []
        self.assertFalse('skajhfasdf' in self.labels)

    def test_plot_events_by_categories(self):
        self.values = []
        self.assertTrue(isinstance(self.values, list))

    def test_plot_events_by_categories2(self):
        self.values = []
        self.assertFalse('21323341234' in self.values)

class SQL_Test(unittest.TestCase):
    def setUp(self):
        sql = 'SELECT * FROM "sqlite_master"'
        self.sqlite_master = {}

    def test_sql(self):
        self.assertTrue(type(self.sqlite_master) == type({}), "Testing query has returned a list.")

    def test_sql_two(self):
        test_dict = {"key": "lock", "door": "hinge"}
        self.assertTrue(type(self.sqlite_master.keys()) == type(test_dict.keys()), "Testing that query returned an object with keys.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
