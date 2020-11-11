import sys

from unittest import TestSuite
from tornado.test.runtests import main

from .models_tests import TestUser


def all():
    suit = TestSuite()
    suit.addTest(TestUser('test_select'))
    suit.addTest(TestUser('test_save_user'))
    # suit.addTest(TestNote('test_get_method'))
    # suit.addTest(TestNote('test_get_all_by_owner_method'))
    return suit


main()
