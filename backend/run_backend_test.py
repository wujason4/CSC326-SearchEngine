import pprint
import os
import unittest
from crawler import crawler
import operator

class TestIndex(unittest.TestCase):

    def test_pretty_print(self):
        bot = crawler(None,"test_page.txt")
        bot.crawl(depth=1)	

        score_list = bot.get_page_rank()

        sorted_score = sorted(score_list.items(), key=operator.itemgetter(1), reverse = True)
        print ("\nPRETTY PRINT RESULTS \n")   
        print "PAGE RANK:"
        pprint.pprint(sorted_score)

if __name__=='__main__':
	unittest.main()
