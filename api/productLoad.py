__author__ = 'Chao'
import webapp2
import logging
from service.productLoadService import ProductLoadService

class ProductLoad(webapp2.RequestHandler):

    def get(self):
        logging.debug(self.request)

        advertiserName = self.request.get('advertiser')
        self.response.out.write('Data loaded successfully')
        ProductLoadService.loadProducts(advertiserName)

class DeleteData(webapp2.RequestHandler):

    def get(self):
        logging.debug(self.request)

        if ProductLoadService.purgeDatastore():
            self.response.out.write('Data Purged Successfully')
        else:
            self.response.out.write('Error occured while purging data')


app = webapp2.WSGIApplication([
                                       ('/load', ProductLoad),
                                       ('/delete', DeleteData)
                                   ], debug=True)