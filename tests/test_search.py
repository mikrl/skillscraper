import json

import pytest
from pytest_mock import mocker

from skillscraper.search import IndeedSearch


def read_text_file(filename: str, ignore_escapes: bool = False):
    with open(filename) as f:
        contents = f.read()
    if ignore_escapes:
        contents = contents.replace("\n", "")
        contents = contents.replace("\t", "")
    return contents


@pytest.fixture(autouse=True)
def indeed_search(*init):
    yield IndeedSearch(*init)


@pytest.fixture
def basic_search_json():
    search_json = read_text_file(
        "./tests/fixtures/swe_waterloo_basic_search.json", ignore_escapes=True
    )
    yield json.loads(search_json)


@pytest.fixture
def basic_search_html():
    yield read_text_file("./tests/fixtures/swe_waterloo_basic_search.html")


class TestIndeedSearch:
    def test_basic_request(mocker, basic_search_json):
        indeed_search.search(basic_fixture["search_parameters"])
        mocker.patch("requests.get")
        requests.get.assert_called_once()
