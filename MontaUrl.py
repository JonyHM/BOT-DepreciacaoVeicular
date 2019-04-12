# -*- coding: utf-8 -*-

class MontaUrl(object):

    def __init__(self):
        self.url = 'http://fipeapi.appspot.com/api/1/'

    def montar(self, arg):
        return self.url + arg
    
    def getUrl(self):
        return self.url