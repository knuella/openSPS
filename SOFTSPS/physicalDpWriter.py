#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import pymongo
from pymongo import MongoClient
from hardwarePlugins import *

testDP3 = {"name": "Relay1",
					"actualValue": 1,
					"state": "don't know!",
					"type": "output",
					"hardwareType": "gnublinRelayIO",
					"hardwareData": {"modulAddress": 0x20,
													 "relayAddress": 3}}

def insertTestDP(dp):
		
	client = MongoClient()
	db = client.test_DB
	IOs = db.IOs
	
	return IOs.insert(dp)


def updateTestDP(dpID, dp):
	
	client = MongoClient()
	db = client.test_DB
	IOs = db.IOs
	
	return IOs.update({"_id": dpID}, dp)

class physicalDpWriter:
	
	def __init__(self):
		self._client = MongoClient()
		self._db = self._client.test_DB
		self._IOs = self._db.IOs
	
	def writeOutput(self, dpID):
		
		dbDp = self._IOs.find_one({"_id": dpID})
		
		physicalDp = getattr(sys.modules[__name__],dbDp['hardwareType']) \
																						(**dbDp['hardwareData'])
		i = 0
		physicalDp.setValue(dbDp['actualValue'])
		while not physicalDp.getGood() and i < 3:
			physicalDp.setValue(dbDp['actualValue'])
			i += 1
		
		if i >= 3:
			self._IOs.update({'_id': dbDp['_id']}, {"$set": {'state':'Hardware Error'}})
		else:
			self._IOs.update({'_id': dbDp['_id']}, {"$set": {'state':'good'}})
	
	
	def writeAllOutputs(self):
		
		for dpID in self._IOs.find({'type': 'output'},{'_id': 1}):
			self.writeOutput(dpID['_id'])


