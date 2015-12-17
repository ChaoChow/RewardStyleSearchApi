__author__ = 'Chao'

from google.appengine.ext import ndb
from models.modelUtil import ModelUtil
from models.item import Item

class KeywordRoot(ndb.Model):
    pass

class Keyword(ndb.Model):
    product_ids = ndb.StringProperty(indexed=False, repeated=True)
