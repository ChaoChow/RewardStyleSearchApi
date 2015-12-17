__author__ = 'Chao'

import logging
import params
import urllib2
import re
import xml.etree.ElementTree as ET
import cStringIO
from xml.etree.cElementTree import iterparse
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
from models.item import Item
from models.keyword import Keyword
from models.keyword import KeywordRoot

class ProductLoadService:

    @classmethod
    def loadProducts(cls, advertiserName):

        keywordDict = {}
        productList = []
        alphaOnlyPattern = re.compile('([^\s\w]|_)+')

        if not advertiserName:
            return False

        advertiserName = urllib2.quote(advertiserName)

        endpointUrl = params.productUrlRoot + advertiserName + params.productUrlToken
        logging.debug(endpointUrl)

        result = urllib2.urlopen(endpointUrl).read()
        context = iterparse(cStringIO.StringIO(result))

        for event, element in context:
            if element.tag == "item":
                product = cls.createItem(element)
                keywordsList = cls.grabKeywords(element, alphaOnlyPattern)
                cls.saveKeywordsInDict(keywordDict, keywordsList, element[0].text)
                productList.append(product)
                if len(productList) > params.maxBatchEntityInsert:
                    cls.saveItemsAsync(productList)
                    keywordObjects = cls.createKeywordList(keywordDict)
                    cls.saveKeywordsAsync(keywordObjects)
                    keywordDict = {}
                    productList = []


        # # serialize xml to ndb entity
        # for element in xml:
        #     product = cls.createItem(element)
        #     keywordsList = cls.grabKeywords(element, alphaOnlyPattern)
        #     cls.saveKeywordsInDict(keywordDict, keywordsList, element[0].text)
        #     productList.append(product)
        #     if len(productList) > params.maxBatchEntityInsert:
        #         cls.saveItemsAsync(productList)
        #         keywordObjects = cls.createKeywordList(keywordDict)
        #         cls.saveKeywordsAsync(keywordObjects)
        #         keywordDict = {}
        #         productList = []

        cls.saveItemsAsync(productList)
        keywordObjects = cls.createKeywordList(keywordDict)
        cls.saveKeywordsAsync(keywordObjects)

        return True

    @classmethod
    def grabKeywords(cls, element, removeCharPattern):
        keywordList = []

        productName = element[1].text
        if productName:
            wordOnlyText = removeCharPattern.sub(' ', productName)
            keywordList.extend(wordOnlyText.lower().split())

        advertiser = element[3].text
        if advertiser:
            wordOnlyText = removeCharPattern.sub(' ', advertiser)
            keywordList.extend(wordOnlyText.lower().split())

        designer = element[4].text
        if designer:
            wordOnlyText = removeCharPattern.sub(' ', designer)
            keywordList.extend(wordOnlyText.lower().split())

        return keywordList

    @classmethod
    def saveKeywordsInDict(cls, keywordsDict, keywordsList, itemID):
        for keyword in keywordsList:
            itemIdList = keywordsDict.get(keyword, None)
            if not itemIdList:
                itemIdList = [itemID]
                keywordsDict[keyword] = itemIdList
            else:
                itemIdList.append(itemID)

    @classmethod
    def createItem(cls, element):
        return Item(id=element[0].text,
                            product_name=element[1].text,
                              product_url=element[2].text,
                              advertiser=element[3].text,
                              designer=element[4].text,
                              image_url=element[5].text,
                              price=float(element[6].text.replace(',', '')),
                              commission=float(element[7].text.replace(',', '')))

    @classmethod
    def createKeyword(cls, keyword, itemIdList):
        return Keyword(parent=ndb.Key(KeywordRoot, keyword),
                            product_ids=itemIdList
                            )

    @classmethod
    def createKeywordList(cls, keywordsDict):
        keywordList = []
        for key, value in keywordsDict.items():
            keywordList.append(cls.createKeyword(key, value))

        return keywordList

    @classmethod
    @ndb.toplevel
    def saveItemsAsync(cls, productList):
        ndb.put_multi_async(productList)
        pass

    @classmethod
    @ndb.toplevel
    def saveKeywordsAsync(cls, keywords):
        keywordsChunk = []
        for keyword in keywords:
            keywordsChunk.append(keyword)

        ndb.put_multi_async(keywordsChunk)

        return

    @classmethod
    @ndb.toplevel
    def purgeDatastore(cls):
        cls.purgeItems()
        cls.purgeKeywords

        return True

    @classmethod
    @ndb.toplevel
    def purgeItems(cls):
        isMore = True
        nextCursor = Cursor()

        while isMore:
            entries, next_cursor, more = Item.query().fetch_page(params.maxBatchEntityInsert,keys_only=True,start_cursor=nextCursor)
            logging.debug(len(entries))
            ndb.delete_multi_async(entries)



    @classmethod
    @ndb.toplevel
    def purgeKeywords(cls):
        isMore = True
        nextCursor = Cursor()

        while isMore:
            entries, next_cursor, more = Keyword.query().fetch_page(params.maxBatchEntityInsert,keys_only=True,start_cursor=nextCursor)
            logging.debug(len(entries))
            ndb.delete_multi_async(entries)