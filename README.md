# Reward Style Search API
This api searches through a large quantity of products by using keywords. Keywords are any words found in the products "advertiser", "designer", or "product_name". Keywords are indexed in a seperate table from the product items and endpoint /search operates similar to a map reduce with the keyword table used as a map and the consolidating of products as the reduce.

Endpoints

Used to search for products by keywords and if we are searching by multiple keywords to specify if products should all contain every keyword (exclusive) or all products in the datastore that match a single keyword of the many should be retrieved (inclusive)
- http://rewardstyle-1161.appspot.com/search?keywords=MULTIPLE+KEYWORDS+HERE&filter_Style={inclusive|exclusive}

This loads data for any advertiser from RewardStyle's prodcut api
- http://rewardstyle-1161.appspot.com/load?advertiser=SINGLE-ADVERTISER-NAME

This endpoint deletes all data from the datastore
- http://rewardstyle-1161.appspot.com/delete
