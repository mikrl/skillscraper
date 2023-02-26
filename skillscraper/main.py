import argparse
from enum import Enum
import logging
from typing import Optional

from skillscraper.aggregator import Aggregator
from skillscraper.indeed_spider import IndeedSpider


class LogLevel(Enum):
    WARNING = 0
    INFO = 1
    DEBUG = 2

def main(job_title: str, location: str, outfile: Optional[str] = None, scrape_only: bool = False):
    
    spider = IndeedSpider(job_title, location)
    spider.crawl()

    if scrape_only:
        if outfile:
            spider.save(outfile)
        else:
            print(spider.get_serialized_results())       

    else:
        results  = spider.get_serialized_results()
        aggregator = Aggregator(results)
        aggregator.process_results(upto_n=4)
        
        if outfile:
            aggregator.save(outfile)
        
        else:
            print(aggregator.get_serialized_results())
            


if __name__ == "__main__":
    # Define command line arguments
    parser = argparse.ArgumentParser(description='Scrape job postings from the internet and turn them into ngrams.')
    parser.add_argument('title', metavar='title', type=str, help='Job title to search for')
    parser.add_argument('location', metavar='location', type=str, help='Location to search in')
    parser.add_argument('-v', '--verbosity', type=int, default=1,
                        help='verbosity level (0 = WARNING, 1 = INFO, 2 = DEBUG)')
    parser.add_argument('-o', '--output', type=str, default='',
                        help='Output file path. If not specified, results will be printed to the terminal')
    parser.add_argument("--scrape-only", action="store_true", help="Only scrape the jobs and do not process the output further. Will save jobs if outfile is specified")

    # Parse arguments and call main function
    args = parser.parse_args()

    log_level = LogLevel(args.verbosity).name
    
    if log_level == LogLevel.WARNING.name:
        logging.getLogger().setLevel(logging.WARNING)
    
    elif log_level == LogLevel.INFO.name:
        logging.getLogger().setLevel(logging.INFO)
    
    elif log_level == LogLevel.DEBUG.name:
        logging.getLogger().setLevel(logging.DEBUG)

    main(args.title, args.location, args.output, args.scrape_only)

