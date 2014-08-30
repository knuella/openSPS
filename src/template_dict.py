from os.path import getmtime, join as pathjoin 
from os import listdir, walk as dirwalk
import json

class TemplateDict(dict):
    def __init__(self, import_path, dict_args):
        self.import_path = import_path
        super().__init__(dict_args)

    def is_modified_path(self):
        return getmtime(self.import_path) > self.get_last_loaded_mtime()

    def get_last_loaded_mtime(self):
        last = 0
        for name, mtime in self.items():
            if last < mtime:
                last = mtime
        return last

    def is_modified(self, name, mtime):
        itempath = pathjoin(self.import_path, name)
        return getmtime(itempath) > mtime
    
    def get_modified(self):
        modified = []
        if self.is_modified_path():
            for name, mtime in self.items():
                if self.is_modified(name, mtime):
                    modified.append(self.read_file(name))
        return modified

    def get_not_listed(self):
        not_listed = []
        if self.is_modified_path():
            root, dirs, names = next(dirwalk(self.import_path))
            for name in names:
                if name not in self:
                    not_listed.append(self.read_file(name))
        return not_listed

    def get_deleted(self):
        deleted = []
        if self.is_modified_path():
            root, dirs, names = next(dirwalk(self.import_path))
            for name, mtime in self.items():
                if name not in names:
                    data= {'meta_data': {'name': name, \
                                         'modification_time':''}}
                    deleted.append(data)
        return deleted

    def read_file(self, name):
        filepath = pathjoin(self.import_path, name)
        raw_data = open(filepath)
        try:
            data = json.load(raw_data)
        except ValueError:
            raise ValueError(name)
        try:
            data['meta_data']['name'] = name
            data['meta_data']['modification_time'] = getmtime(filepath)
        except KeyError:
            data['meta_data'] = {'name': name, \
                                 'modification_time':getmtime(filepath)}
        return data


