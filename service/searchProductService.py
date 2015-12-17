__author__ = 'Chao'

import logging
from google.appengine.ext import ndb
from models.keyword import KeywordRoot
from models.keyword import Keyword
from models.item import Item

class SearchProductService:

    @classmethod
    def searchProducts(cls, keywordsList, isInclusive):
        itemsInDictForm = []

        if isInclusive:
            logging.debug('getting inclusive')
            allItemIds = cls.getAllItemKeysForKeywordListInclusive(keywordsList)
        else:
            logging.debug('getting exclusive')
            allItemIds = cls.getAllItemKeysForKeywordListExclusive(keywordsList)

        itemKeys = cls.convertItemIDsToKeys(allItemIds)
        items = ndb.get_multi(itemKeys)

        for item in items:
            itemsInDictForm.append(item.to_dict())

        return itemsInDictForm


    @classmethod
    def convertItemIDsToKeys(cls, allItemIds):

        keyList = []
        for itemId in allItemIds:
            key = ndb.Key(Item, itemId)
            keyList.append(key)

        return keyList


    @classmethod
    def getAllItemKeysForKeywordListInclusive(cls, keywordsList):

        allItemIds = []
        for keyword in keywordsList:
            itemsForSingleKeyword = cls.getItemKeysForKeyword(keyword)
            allItemIds = list(set(itemsForSingleKeyword)|set(allItemIds))

        return allItemIds


    @classmethod
    def getAllItemKeysForKeywordListExclusive(cls, keywordsList):

        allItemIds = []
        for keyword in keywordsList:
            itemsForSingleKeyword = cls.getItemKeysForKeyword(keyword)

            # gets the array started or union will always have nothing
            if len(allItemIds) == 0:
                allItemIds = itemsForSingleKeyword

            allItemIds = list(set(allItemIds)&set(itemsForSingleKeyword))

        return allItemIds


    @classmethod
    def getItemKeysForKeyword(cls, keyword):

        itemIds = []

        rootKey = ndb.Key(KeywordRoot, keyword)
        keywordObjects = Keyword.query(ancestor=rootKey).fetch()

        logging.debug(len(keywordObjects))

        for keywordObject in keywordObjects:
            itemIds.extend(keywordObject.product_ids)

        return itemIds