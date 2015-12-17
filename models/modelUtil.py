__author__ = 'Chao'

class ModelUtil(object):
    def to_dict(self):
        result = super(ModelUtil,self).to_dict()
        result['product_id'] = self.key.id() #get the key as a string
        return result