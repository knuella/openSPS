#!/usr/bin/python
# -*- coding: ascii -*-
import pymongo
from pymongo import MongoClient
from output import *


class DPHolder:
    
    def __init__(self):    
        self.outputs = {}
        self.get_from_db()
    
    def get_from_db(self):
        db_client = MongoClient()
        db_outputs = db_client.ios.outputs        
        output_names = db_outputs.distinct('name')
        
        for output_name in output_names:
            self.outputs[output_name] = OutputDP(output_name) 
    
    def write_all_physical_values(self):
        for key in self.outputs:
            self.outputs[key].write_physical_value()
    
    def update_all_to_db(self):        
        for key in self.outputs:
            self.outputs[key].update_to_db()


def add_my_dps():
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
