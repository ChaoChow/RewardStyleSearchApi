__author__ = 'Chao'

from google.appengine.ext import ndb
from models.modelUtil import ModelUtil

class Item(ModelUtil, ndb.Model):
    product_name = ndb.StringProperty(indexed=False)
    product_url = ndb.StringProperty(indexed=False)
    advertiser = ndb.StringProperty(indexed=False)
    designer = ndb.StringProperty(indexed=False)
    image_url = ndb.StringProperty(indexed=False)
    price = ndb.FloatProperty(indexed=False, default=0)
    commission = ndb.FloatProperty(indexed=False, default=0)
