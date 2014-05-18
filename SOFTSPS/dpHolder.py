#!/usr/bin/python
# -*- coding: ascii -*-
import pymongo
from pymongo import MongoClient
from OutputDP import *

class dpHolder:
	
	def __init__(self):
		
		self.outputs = {}
		self.getfromDB()
	
	
	def getfromDB(self):
		
		dbClient = MongoClient()
		dbOutputs = dbClient.IOs.Outputs
		
		outputNames = dbOutputs.distinct('name')
		
		for outputName in outputNames:
			self.outputs[outputName] = OutputDP(outputName) 
	
	
	def writeAllPhysicalValues(self):
		
		for key in self.outputs:
			self.outputs[key].writePhysicalValue()
	
	
	def updateAllToDB(self):
		
		for key in self.outputs:
			self.outputs[key].updateToDB()



def addMyDPs():
	client = MongoClient()
	outputs = client.IOs.Outputs
	for k in range(0,2):
		for i in range(1,5):
			outputs.save({"name": "Relay" + (str)(i+4*k),
										"actualValue": 0,
										"state": "don't know!",
										"type": "binary output",
										"hardwareType": "gnublinRelayIO",
										"hardwareData": {"modulAddress": 32+k,
																		 "relayAddress": i}
										})
	
	for i in range(0,4):
		outputs.save({"name": "Dac" + (str)(i+1),
									"actualValue": 0,
									"unit": "V",
									"state": "don't know!",
									"type": "analog output",
									"hardwareType": "gnublinDacIO",
									"hardwareData": {"dacAddress": i,
																	 "scalingType": "linearScaler",
																	 "scalingData": {"y1":0,
																									 "y2":2900,
																									 "x1":0,
																									 "x2":10}
																	}
									})
