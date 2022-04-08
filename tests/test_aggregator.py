from unittest import TestCase

import skillscraper


class TestAggregator(TestCase):
    tdict = {"a": 5, "b": 3}
    testlst = ["a", "b", "c"]

    print(tdict)
    tdict = aggregate(testlst, tdict)
    print(tdict)
    print(aggregate(testlst, tdict))

    raise NotImplementedError
