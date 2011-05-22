import _setup

import unittest

from nose.tools import (assert_equals, assert_true)

import utils

from github2.client import Github


class UserProperties(unittest.TestCase):
    """Test user property handling"""
    def setUp(self):
        utils.set_http_mock()
        self.client = Github()

    def tearDown(self):
        utils.unset_http_mock()

    def test_user(self):
        user = self.client.users.show('defunkt')
        assert_equals(user.blog, 'http://chriswanstrath.com/')
        assert_equals(user.company, 'GitHub')
        assert_equals(user.email, 'chris@wanstrath.com')
        assert_equals(user.location, 'San Francisco')
        assert_equals(user.login, 'defunkt')
        assert_equals(user.name, 'Chris Wanstrath')

    def test_meta(self):
        user = self.client.users.show('defunkt')
        # Difficult to handle created_at attribute as its content varies
        # depending on API path.
        #assert_equals(user.created_at,
        #              datetime.datetime(2007, 10, 19, 22, 24, 19))
        assert_equals(user.followers_count, 2593)
        assert_equals(user.following_count, 212)
        assert_equals(user.gravatar_id, 'b8dbb1987e8e5318584865f880036796')
        assert_equals(user.id, 2)
        assert_equals(user.public_gist_count, 277)
        assert_equals(user.public_repo_count, 90)

    def test_followers(self):
        assert_equals(len(self.client.users.followers('defunkt')), 2593)

    def test_following(self):
        assert_equals(len(self.client.users.following('defunkt')), 212)


class UserQueries(unittest.TestCase):
    """Test user querying """
    def setUp(self):
        utils.set_http_mock()
        self.client = Github()

    def tearDown(self):
        utils.unset_http_mock()

    def test_search(self):
        assert_equals(repr(self.client.users.search('James Rowe')),
                      '[<User: JNRowe>, <User: wooki>]')

    def test_search_by_email(self):
        user = self.client.users.search_by_email('jnrowe@gmail.com')
        assert_equals(repr(user), '<User: JNRowe>')