#!/usr/bin/python
import pymongo
from pymongo import MongoClient
from opensps_database import MongoDBTemplateCollection
import json
from os import listdir
from os.path import isfile, join
import re

class ConfigurationManager:
    
    def __init__(self, massagemanager_address, config_db="opensps_config"):
        self.connect_to_db(config_db)
        #connect_to_massagemanager(massagemanager_address, config_db=opensps_conf)
    
    def connect_to_db(self, config_db):
        self._db_client = MongoClient()
        self.modules = MongoDBTemplateCollection(
            self._db_client[config_db].module_templates,
            self._db_client[config_db].modules)
        self.dps = MongoDBTemplateCollection(
            self._db_client[config_db].datapoint_templates,
            self._db_client[config_db].datapoints)
    
    def reload_plugin_templates(self, plugin_path="hardware_plugins"):
        plugin_files = [ f for f in listdir(plugin_path) 
                       if isfile(join(plugin_path,f)) ]
    
        for f in plugin_files:
            if re.search("template.json", f):
                json_data = open(plugin_path + '/' + f)
                data = json.load(json_data)
                if not self.dps.get_templatename_list(
                        {'template_name': data['template_name']}):
                    self.dps.save_template(data)

