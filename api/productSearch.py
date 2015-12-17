__author__ = 'Chao'
import webapp2
import logging
import params
import json
from service.searchProductService import SearchProductService

class ProductSearch(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        logging.debug(self.request)

        # keyword string is required
        keywordString = self.request.get('keywords', None)
        filter = self.request.get('filter_style', None)

        if keywordString is None:
            self.response.out.write('Keywords are required for product search')
            return
        else:
            keywords = keywordString.lower().split(' ')

        logging.debug(keywords)

        # optional filter
        if filter and filter.lower() == params.includeFilterName:
            allItems = SearchProductService.searchProducts(keywords, True)
        elif filter and filter.lower() == params.excludeFilterName:
            allItems = SearchProductService.searchProducts(keywords, False)
        else:
            allItems = SearchProductService.searchProducts(keywords, True)

        self.response.write(json.dumps(allItems))

app = webapp2.WSGIApplication([
                                       ('/search', ProductSearch)
                                   ], debug=True)