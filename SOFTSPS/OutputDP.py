#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import pymongo
from pymongo import MongoClient
from hardwarePlugins import *


class OutputDP:
	
	def __init__(self, dpName):
		self._client = MongoClient()
		self._outputs = self._client.IOs.Outputs
		
		self._dp = self._outputs.find_one({'name': dpName})
		if self._dp == None:
			raise InputError("Can't find DP with the Name " + dpName)
		
		self._physicalDp = getattr(sys.modules[__name__],self._dp['hardwareType']) \
											 (**self._dp['hardwareData'])	
	
	
	def setValue(self, toSetValue):
		
		self._dp['actualValue'] = toSetValue
	
	
	def writePhysicalValue(self):
		
		i = 0
		self._physicalDp.setValue(self._dp['actualValue'])
		
		while not self._physicalDp.getGood() and i < 3:
			self._physicalDp.setValue(dp['actualValue'])
			i += 1
		
		if i >= 3:
			self._dp['state'] = 'Hardware Error'
		
		else:
			self._dp['state'] = 'good'
	
	
	def updateToDB(self):
		
		self._outputs.update({'_id': self._dp['_id']}, \
										 {'$set': {'state': self._dp['state'], \
															 'actualValue': self._dp['actualValue']}})


