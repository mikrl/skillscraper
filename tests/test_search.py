import json

import pytest
from pytest_mock import mocker

from skillscraper.search import IndeedSearch

def read_text_file(filename: str):
    with open(filename) as f:
        return f.readlines()



class TestIndeedSearch:

    @pytest.fixture(autouse=True)
    def indeed_search(*init):
        yield IndeedSearch(*init)
    
    @pytest.fixture
    def basic_search_json():
        yield json.load('./fixtures/swe_waterloo_basic_search.json')

    @pytest.fixture
    def basic_search_html():
        yield read_text_file('./fixtures/swe_waterloo_basic_search.html')
    
    def test_basic_request(mocker, basic_search_json):            
        indeed_search.search(basic_fixture['search_parameters'])
        mocker.patch('requests.get')
        requests.get.assert_called_once()

    











