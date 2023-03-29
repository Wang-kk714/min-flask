import unittest
from flask_backend.redis_service import Redis

class RedisTestCase(unittest.TestCase):

    def setUp(self):
        self.redis = Redis()
        self.string_key = 'my_string'
        self.list_key = 'my_list'
        self.set_key = 'my_set'
        self.hash_name = 'my_hash'
        self.sorted_set_key = 'my_sorted_set'
    
    def tearDown(self):
        self.redis._redis.flushdb()

    def test_string(self):
        self.assertTrue(self.redis.add_string(self.string_key, 'hello', expire_time=5))
        self.assertEqual(self.redis.select_string(self.string_key), 'hello')
        self.assertTrue(self.redis.update_string(self.string_key, 'world', expire_time=5))
        self.assertEqual(self.redis.select_string(self.string_key), 'world')
        self.assertTrue(self.redis.remove_string(self.string_key))
        self.assertIsNone(self.redis.select_string(self.string_key))

    def test_list(self):
        self.assertTrue(self.redis.add_list(self.list_key, 'item1', 'item2', 'item3', expire_time=5))
        self.assertEqual(self.redis.select_list(self.list_key, index=0), 'item1')
        self.assertTrue(self.redis.update_list(self.list_key, 0, 'item1', expire_time=5))
        self.assertTrue(self.redis.remove_list(self.list_key, value='item1'))


    def test_set(self):
        self.assertTrue(self.redis.add_set(self.set_key, 'item1', 'item2', 'item3', expire_time=5))
        self.assertEqual(self.redis.select_set(self.set_key), {'item3', 'item2', 'item1'})
        self.assertTrue(self.redis.remove_set(self.set_key, 'item1', 'item2'))

    def test_hash(self):
        self.assertTrue(self.redis.add_hash(self.hash_name, "key1", {'item1': 'value1', 'item2': 'value2'}, expire_time=5))
        self.assertTrue(self.redis.update_hash(self.hash_name, "key1", {'item1': 'value2', 'item2': 'value4'}, expire_time=5))
        self.assertEqual(self.redis.select_hash(self.hash_name, "key1"), {'item1': 'value2', 'item2': 'value4'})
        self.assertTrue(self.redis.remove_hash(self.hash_name, "key1"))
