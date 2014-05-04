#!/usr/bin/python
# -*- coding: ascii -*-
import pymongo
from pymongo import MongoClient
import datetime
import time

client = MongoClient()
db = client.test_DB
IOs = db.IOs

# ===========================
# setzen der Hardwareadressen
# ===========================

relay1 = {'name': 'Relay1'}
#relay2 = {'name': 'Relay2'}

#dac1 = gnublin.gnublin_module_dac() 


# ==================
# Steuerungsprogramm
# ==================

startZeit1 = datetime.time(10, 45, 0)
stopZeit1 = datetime.time(13, 20, 0)


jetzt = datetime.datetime.now()

if ((jetzt.time() > startZeit1) and (jetzt.time() < stopZeit1)):
	IOs.update(relay1, {"$set": {'actualValue':'1'}})
else:
	IOs.update(relay1, {"$set": {'actualValue':'0'}})


#startZeit2 = datetime.time(10,45, 0)
#stopZeit2 = datetime.time(14, 00, 0)
#schrittweite = 16
#helligkeit_aus = 0
#helligkeit_ein = 4095
#helligkeit = dac1.read(0)
#
#
#
#if ((jetzt.time() > startZeit2) and (jetzt.time() < stopZeit2)):
#
#	relay1.switchPin(2 ,1)
#	
#	if (dac1.read(0) < (helligkeit_ein - schrittweite)):
#		helligkeit += schrittweite
#		dac1.write(0, helligkeit)
#
#	else:
#		helligkeit = helligeit_ein
#		dac1.write(helligkeit)
#
#
#else:
#	
#	if (dac1.read(0) > (helligkeit_aus + schrittweite)):
#		helligkeit -= schrittweite
#		dac1.write(0, helligkeit)
#
#	else:
#		helligkeit = helligkeit_aus
#		dac1.write(0, helligkeit)
#		relay1.switchPin(2 ,0)
#
