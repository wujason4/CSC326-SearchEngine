import unittest
from crawler import crawler

class TestIndex(unittest.TestCase):

	def test_empty_url(self):
		print ("Test empty inverted and resolved inverted index\n")
		bot = crawler(None,"")
		bot.crawl(depth=1)
		
		self.assertEqual(bot.get_inverted_index(),{})
		self.assertEqual(bot.get_resolved_inverted_index(), {})
		print ("=====================\n")

	def test_one_url(self):
		print ("Test inverted and resolved inverted index with one URL \n")
		bot = crawler(None,"test_page1.txt")
		bot.crawl(depth=1)		

		self.assertEqual(bot.get_inverted_index(),{1: set([1]), 2: set([1]), 3: set([1]), 4: set([1]), 5: set([1])})
		self.assertEqual(bot.get_resolved_inverted_index(), {u'test': set(['http://localhost:8080/page1.tpl']), u'paragraph': set(['http://localhost:8080/page1.tpl']), u'my': set(['http://localhost:8080/page1.tpl']), u'page': set(['http://localhost:8080/page1.tpl']), u'first': set(['http://localhost:8080/page1.tpl'])})
		print ("=====================\n")
	
	def test_two_urls(self):
		print ("Test inverted and resolved inverted index with two URLs\n")
		bot = crawler(None,"test_page2.txt")
		bot.crawl(depth=1)

		self.assertEqual(bot.get_inverted_index(),{1: set([1, 2]), 2: set([1]), 3: set([1, 2]), 4: set([1, 2]), 5: set([1, 2]), 6: set([2])})
		self.assertEqual(bot.get_resolved_inverted_index(), {u'second': set(['http://localhost:8080/page2.tpl']), u'paragraph': set(['http://localhost:8080/page2.tpl', 'http://localhost:8080/page1.tpl']), u'test': set(['http://localhost:8080/page2.tpl', 'http://localhost:8080/page1.tpl']), u'my': set(['http://localhost:8080/page2.tpl', 'http://localhost:8080/page1.tpl']), u'page': set(['http://localhost:8080/page2.tpl', 'http://localhost:8080/page1.tpl']), u'first': set(['http://localhost:8080/page1.tpl'])})

		print ("=====================\n")
if __name__=='__main__':
	unittest.main()
