#!/usr/bin/python
# -*- coding: ascii -*-
from time import sleep
from dpHolder import dpHolder

dpHolder = dpHolder()

i = 0
while True:
	sleep(.5)
	dpHolder.writeAllPhysicalValues()
	
	i += 1
	if i == 20:
		i = 0
		dpHolder.updateAllToDB()


