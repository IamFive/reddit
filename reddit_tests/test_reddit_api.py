# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
# @author: Five
# Created on 2013-9-20
#

import unittest
from reddit.common.tools.reddit_cli import rc


class TestRedditApi(unittest.TestCase):


#    def testName(self):
#
#        subreddit = rc.get_subreddit('python')
#        print subreddit.fullname
#        submissions = subreddit.get_hot(limit=5)
#        print [str(x) for x in submissions]
#
#        submissions = subreddit.get_new(limit=5)
#        print [str(x) for x in submissions]


    def test_get_subreddit(self):
        subreddit = rc.get_subreddit('python')
        submissions = subreddit.get_hot(limit=20)
        for x in submissions:
            print x.author.name

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
