from skillscraper.aggregator import ListingAggregator


class TestListingAggregator:
    tdict = {"a": 5, "b": 3}
    testlst = ["a", "b", "c"]

    print(tdict)
    tdict = aggregate(testlst, tdict)
    print(tdict)
    print(aggregate(testlst, tdict))

    raise NotImplementedError
