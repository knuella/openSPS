#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import pymongo
from pymongo import MongoClient
from hardware_plugins import *


class OutputDP:
    
    def __init__(self, dp_name):
        self._client = MongoClient()
        self._outputs = self._client.ios.outputs
        
        self._dp = self._outputs.find_one({'name': dp_name})
        if self._dp == None:
            raise InputError("Can't find DP with the Name " + dp_name)
        
        self._physical_dp = getattr(
                sys.modules[__name__],
                self._dp['hardware_type'])(**self._dp['hardware_data'])   
    
    def set_value(self, to_set_value): 
        self._dp['actual_value'] = to_set_value
    
    def write_physical_value(self):    
        i = 0
        self._physical_dp.set_value(self._dp['actual_value'])
        
        while not self._physical_dp.get_good() and i < 3:
            self._physical_dp.set_value(self._dp['actual_value'])
            i += 1
        
        if i >= 3:
            self._dp['state'] = 'Hardware Error'
        
        else:
            self._dp['state'] = 'good'
    
    def update_to_db(self):
        self._outputs.update(
            {'_id': self._dp['_id']}, 
            {'$set': 
                {
                    'state': self._dp['state'], 
                    'actual_value': self._dp['actual_value']
                }
            })


