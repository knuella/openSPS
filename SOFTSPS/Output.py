#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import pymongo
from pymongo import MongoClient
from hardwarePlugins import *


binaryOutput1 = {"name": "Relay1",
								 "actualValue": 0,
								 "state": "don't know!",
								 "type": "binary output",
								 "hardwareType": "gnublinRelayIO",
								 "hardwareData": {"modulAddress": 0x20,
																	"relayAddress": 1}}

analogOutput1 = {"name": "Dac1",
								 "actualValue": 0,
								 "unit": "V",
								 "state": "don't know!",
								 "type": "analog output",
								 "hardwareType": "gnublinDacIO",
								 "hardwareData": {"dacAddress": 0,
																	"transformationType": "linearTransformator",
																	"transformationData": {"computal1":0,
																												 "humanReadebal1":0,
																												 "computal2":2700,
																												 "humanReadebal2":10}}}



class OutputDP:
	
	def __init__(self, dpID):
		self._client = MongoClient()
		self._IOs = self._client.testDB.IOs
		
		self._dp = IOs.find_one({'_id': dpID})
		
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
		
		self._IOs.update({'_id': dp['_id']}, \
										 {'$set': {'state': dp['state'], \
															 'actualValue': dp['actualValue']}})


