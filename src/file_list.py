from os.path import getmtime, join as pathjoin 
from os import listdir, walk as dirwalk

class FileList(list):
    def __init__(self, import_path, **list_args):
        self.import_path = import_path
        super().__init__(list_args)

    def filenames(self):
        files = []
        for item in self:
            files.append(item['filename'])
        return files

    def append(self, item):
        data = {}
        try:
            data['filename'] = item['filename']
            data['mtime'] = item['modification_time']
            super().append(data)
        except KeyError:
            TypeError('item must be e dict of "filename" and ' + \
                      '"modification_time"')

    def is_modified_path(self):
        return getmtime(self.import_path) > self.get_last_loaded_mtime()

    def get_last_loaded_mtime(self):
        last = 0
        for item in self:
            if last < item['mtime']:
                last = item['mtime']
        return last

    def is_modified(self, item):
        itempath = pathjoin(self.import_path, item['filename'])
        return getmtime(itempath) > item['mtime']
    
    def get_modified(self):
        modified = []
        if self.is_modified_path():
            for item in self:
                if self.is_modified(item):
                    data = self.get_file_content(item['filename'])
                    data['meta_data'] = self.get_meta_data(item['filename'])
                    modified.append(data)
        return modified

    def get_not_listed(self):
        not_listed = []
        if self.is_modified_path():
            root, dirs, filenames = next(dirwalk(self.import_path))
            for filename in filenames:
                if filename not in self.filenames():
                    data = self.get_file_content(filename)
                    data['meta_data'] = self.get_meta_data(filename)
                    not_listed.append(data)
        return not_listed

    def get_deleted(self):
        deleted = []
        if self.is_modified_path():
            root, dirs, filenames = next(dirwalk(self.import_path))
            for listed_name in self.filenames():
                if listed_name not in filenames:
                    data = self.get_file_content(filename)
                    data['meta_data'] = self.get_meta_data(filename)
                    deleted.append(data)
        return deleted

    def get_meta_data(self, filename):
        filepath = pathjoin(self.import_path, filename)
        data = {'filename': filename}
        try:
            data['modification_time'] = getmtime(filepath)
        except FileNotFoundError:
            data['modification_time'] = ''
        return data

    def get_file_content(self, filename):
        """ Should return a dict with the content of the file or other file
        information.

        For example: 
        - return a dict, when the file is a json file
        - return the import path, when the file is a python script
        """
        return {}

