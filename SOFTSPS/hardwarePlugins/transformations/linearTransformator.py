#!/usr/bin/python
# -*- coding: ascii -*-

class linearTransformator:
	
	def __init__(self, computal1, humanReadebal1, computal2, humanReadebal2):
		
		self._m = ((float)(computal2) - (float)(computal1)) / \
							((float)(humanReadebal2) - (float)(humanReadebal1))
		self._n = (float)(computal1) - (float)(humanReadebal1) * self._m
	
	def getComputal(self, humanReadebal):
		
		return self._m * humanReadebal + self._n
	
	
	def getHumanReadebal(self, computal):
		
		return (computal - self._n) / self._m
	
	def getM(self):
		
		return self._m
	
	def getN(self):
		
		return self._n

