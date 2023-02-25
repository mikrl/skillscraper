import json
import logging


from skillscraper.nlp_utils import map_ngrams, reduce_ngrams

class Aggregator:

    def __init__(self, results=None):
        self.results = json.loads(results) if results else results

    def get_ngrams(self, n):
        ngram_list = []
        logging.info(f"Turning {len(self.results)} job listings into {n}-grams")
        for result in self.results:
            listing_text = result.get("content")
            ngram_list.extend(map_ngrams(listing_text, n))
        ngrams = reduce_ngrams(ngram_list)
        logging.info(f"Extracted {len(ngrams)} distinct {n}-grams")
        return ngrams

    def load_results_from_file(self, filename):
        with open(filename, 'r') as result_file:
            self.results = json.load(result_file)
        logging.info(f"Read results from {filename}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aggregator = Aggregator()
    aggregator.load_results_from_file('./swe_waterloo_poc.json')
    one_grams = aggregator.get_ngrams(n=1)
    two_grams = aggregator.get_ngrams(n=2)
    three_grams = aggregator.get_ngrams(n=3)

    for i in range(1,4):
        print(aggregator.get_ngrams(i))