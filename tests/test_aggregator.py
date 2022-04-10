import pytest

from skillscraper.aggregator import Aggregator


@pytest.fixture(autouse=True)
def aggregator(*init):
    yield Aggregator(*init)


@pytest.fixture
def basic_listing():
    listing = "the good, the bad, and the ugly"
    yield listing


@pytest.fixture
def listing_1grams():
    mapped = {"the": 3, "good": 1, "bad": 1, "and": 1, "ugly": 1}
    yield mapped


@pytest.fixture
def listing_2grams():
    mapped = {
        "the good": 1,
        "good the": 1,
        "the bad": 1,
        "bad and": 1,
        "and the": 1,
        "the ugly": 1,
    }
    yield mapped


@pytest.fixture
def listing_3grams():
    mapped = {
        "the good the": 1,
        "good the bad": 1,
        "the bad and": 1,
        "bad and the": 1,
        "and the ugly": 1,
    }
    yield mapped


class TestListingAggregator:
    def test_1gram_mapping(basic_listing, listing_1grams):
        aggregated = aggregator.aggregate_ngrams(basic_listing, 1)
        assert aggregated == listing_1grams

    def test_2gram_mapping(basic_listing, listing_2grams):
        aggregated = aggregator.aggregate_ngrams(basic_listing, 2)
        assert aggregated == listing_2grams

    def test_3gram_mapping(basic_listing, listing_3grams):
        aggregated = aggregator.aggregate_ngrams(basic_listing, 3)
        assert aggregated == listing_3grams
