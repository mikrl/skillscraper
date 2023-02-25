import contextlib
import logging
import urllib.parse
from http.client import HTTPConnection


def debug_requests_on(loglevel=logging.DEBUG):
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(loglevel)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(loglevel)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

@contextlib.contextmanager
def debug_requests(loglevel=None):
    '''Use with 'with'!'''
    debug_requests_on(loglevel)
    yield
    debug_requests_off()

class IndeedSite:
    
    def __init__(self, scheme, domain):
        self.scheme = scheme
        self.domain=domain

    def url_formatter(self, url):
        url = urllib.parse.quote(url, safe='=?&/:')
        url = url.replace(' ', '+')
        return url

    def get_search_url(self, job_title, location):
        search_url = f"{self.scheme}{self.domain}/jobs?q={job_title}&l={location}"
        return self.url_formatter(search_url)

    def get_job_post_url(self, job_key):
        # Will look something like jk=d4fb8e699210c7df
        job_post_url = f"{self.scheme}{self.domain}/viewjob?jk={job_key}"
        return self.url_formatter(job_post_url)