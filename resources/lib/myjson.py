# -*- coding: utf-8 -*-
import json
import io
import requests
import xbmc, xbmcvfs, xbmcaddon
from addon import Addon

#TODO delete import Addon?

class MyJson:

    def __init__(self):
        self.ad = Addon()
        self.create_dirs()
        self.copy_db()

    def read_json(self, db_file):
        xbmc.log(self.ad.log_msg + '!READ JSON!', 1)
        xbmc.log(self.ad.log_msg + 'File: '+db_file, 1)
        if xbmcvfs.exists(db_file):
            xbmc.log(self.ad.log_msg+'File Exists', 1)
            with open(db_file) as f:
                try:
                    data = json.load(f)
                    f.close()
                except ValueError:
                    data = []
        else:
            xbmc.log(self.ad.log_msg + 'File Does Not Exist', 1)
            data = []
        return data

    def write_json(self, db_file, data):
        xbmc.log(self.ad.log_msg + '!WRITE JSON!', 1)
        xbmc.log(self.ad.log_msg + 'File: ' + db_file, 1)
        self.create_dir(self.addon_data_dir)
        self.create_dir(self.addon_db_dir)
        with io.open(db_file, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(data, ensure_ascii=False)))
            f.close()

    def check_dir(self, directory):
        return xbmcvfs.exists(directory)

    def create_dir(self, directory):
        if not xbmcvfs.exists(directory):
            xbmcvfs.mkdir(directory)

    def create_dirs(self):
        self.create_dir(self.ad.data_dir)
        self.create_dir(self.ad.db_dir)

    def copy_db(self):
        if not self.check_dir(self.ad.db_file):
            xbmc.log(self.ad.resources_db_file)
            xbmc.log(str(xbmcvfs.copy(self.ad.resources_db_file, self.ad.db_file)))

    def get_json(self, uri):
        r = requests.get(uri)
        data = r.json()
        r.connection.close()
        return data


