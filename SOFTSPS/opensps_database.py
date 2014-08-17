#!/usr/bin/python
import pymongo
from pymongo import MongoClient

class MongoDBTemplateCollection:

    def __init__(self, template_collection, object_collection):
        self._templates = template_collection
        self._objects = object_collection

    # Methoden, die auf Objekte wirken
    def save_object(self, filled_template):
        object_id = self._objects.save(filled_template)
        return object_id

    def get_object(self, value, find_field='_id'):
        filled_template = self._objects.find_one({find_field:value})
        return filled_template
    
    def update_object(self, find_dict, filled_template):
        report = self._templates.update(find_dict, filled_template)
        return report

    def delete_object(self, object_id):
        report = self._templates.delete(object_id)
        return report

    def get_objectname_list(self, find_key_value={}, result_field='divice_params["name"]'):
        object_list = self._objects.find(find_key_value)
        objectname_list = []
        for objectn in object_list:
            objectname_list.append(objectn[result_field])
        return objectname_list

    # Mehtoden, die auf Templates wirken
    def save_template(self, template):
        template_id = self._templates.save(template)
        return template_id

    def get_template(self, value, find_field='template_name'):
        template = self._templates.find_one({find_field:value})
        return template

    def delete_template(self, template_id):
        report = self._templates.delete(template_id)
        return report
    
    def update_template(self, find_dict, template):
        report = self._templates.update(find_dict, template)
        return report

    def get_templatename_list(self, find_key_value={}, result_field='template_name'):
        template_list = self._templates.find(find_key_value)
        templatename_list = []
        for template in template_list:
            templatename_list.append(template[result_field])
        return templatename_list


