#!/usr/bin/python
# -*- coding: ascii -*-
import pymongo
from pymongo import MongoClient
from output import *


class DPHolder:
    """ Creates lists of instaces from OutputDP-Class or InputDP-Class.
    The class depends on the collecion in that the datapoints are. 
    Contains methodes to do manipulations on all the datapoints in the list,
    whith assume that the instances have the same methodes.

    Attributes:
        _outputs (dict): dict of datapoint names (kay) and instances of the
            datapoint (value).
    """

    def __init__(self):    
        """ Inizialize the lists by calling the method "get_from_db" """
        self._outputs = {}
        self.get_from_db()
    
    def get_from_db(self):
        """ Reads the names of the datapoints in the collections and creates one
        list for every collection. 
        Actually only the list "_outputs".
        """
        db_client = MongoClient()
        db_outputs = db_client.ios.outputs        
        output_names = db_outputs.distinct('name')
        
        for output_name in output_names:
            self._outputs[output_name] = OutputDP(output_name) 
    
    def write_all_physical_values(self):
        """ Write all the values of the datapoints in the list "_outputs",
        witch have changed, to the hardware.
        """
        for key in self._outputs:
            self._outputs[key].write_physical_value()
    
    def update_all_to_db(self):        
        """ Write all the values and the state of the datapoints in the list "_outputs",
        witch have changed, to the database.
        """
        for key in self._outputs:
            self._outputs[key].update_to_db()


def add_my_dps():
    """ Testfunction.
    Add some datapoints to the database. 
    """
    client = MongoClient()
    outputs = client.ios.outputs

    for k in range(0, 2):
        for i in range(1, 5):
            outputs.save(
                {
                    "name": "Relay" + (str)(i + 4*k),
                    "actual_value": 0,
                    "state": "don't know!",
                    "type": "binary output",
                    "hardware_type": "GnublinRelayIO",
                    "hardware_data": 
                        {
                            "modul_address": 32 + k,
                            "relay_address": i
                        }
                }
            )
    
    for i in range(0, 4):
        outputs.save(
            {
                "name": "Dac" + (str)(i + 1),
                "actual_value": 0,
                "unit": "V",
                "state": "don't know!",
                "type": "analog output",
                "hardware_type": "GnublinDacIO",
                "hardware_data": 
                    {
                        "dac_address": i,
                        "scaling_type": "LinearScaler",
                        "scaling_data": 
                            {
                                "y1":0,
                                "y2":2900,
                                "x1":0,
                                "x2":10
                            }
                    }
            }
        )
