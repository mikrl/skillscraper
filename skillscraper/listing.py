import urllib

class Listing:
    pass


class IndeedListing(Listing):

    def get_listing_html(self, listing_url):
        req = urllib.request.Request(listing_url)

        with urllib.request.urlopen(req) as response:
            raw_html = response.read()

        return raw_html
