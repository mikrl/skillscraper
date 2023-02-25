import json
import logging

from skillscraper.aggregator import Aggregator
from skillscraper.indeed_spider import IndeedSpider

def main():
    job_title = "Software Developer" 
    location = "Waterloo,ON"
    logging.basicConfig(level=logging.INFO)
    spider = IndeedSpider(job_title, location)
    spider.crawl()
    results = spider.get_serialized_results()

    aggregator = Aggregator(results)

    one_grams = aggregator.get_ngrams(n=1)
    two_grams = aggregator.get_ngrams(n=2)
    three_grams = aggregator.get_ngrams(n=3)

    aggregated_json = {"1grams": one_grams, "2grams": two_grams, "3grams": three_grams}
    print(json.dumps(aggregated_json, indent=4))

if __name__ == "__main__":
    main()
