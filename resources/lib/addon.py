import xbmcaddon
import xbmc
import os


class Addon:

    def __init__(self):
        self.id = 'script.skip.intro'
        self.addon = xbmcaddon.Addon(id=self.id)
        self.path = xbmc.translatePath(self.addon.getAddonInfo('path'))
        self.resources_dir = os.path.join(self.path, 'resources') + '\\'
        self.resources_db_file = os.path.join(self.resources_dir, 'data.json')
        self.data_dir = xbmc.translatePath(self.addon.getAddonInfo('profile'))
        self.db_dir = xbmc.translatePath(os.path.join(self.data_dir, 'db'))
        self.db_file = xbmc.translatePath(os.path.join(self.db_dir, 'data.json'))
        self.log_msg = self.id + ' - '



    def get_state_intro_service(self):
        ret = False

        if self.addon.getSetting('state_intro_service') == 'true':
            ret = True
        return ret

    def get_state_outro_auto_service(self):
        ret = False

        if self.addon.getSetting('state_outro_auto_service') == 'true':
            ret = True
        return ret

    def get_state_outro_static_service(self):
        ret = False

        if self.addon.getSetting('state_outro_static_service') == 'true':
            ret = True
        return ret

    def get_state_outro_auto_service_shows_only(self):
        ret = False

        if self.addon.getSetting('state_outro_auto_service_shows_only') == 'true':
            ret = True
        return ret

    def get_state_local_db(self):
        ret = False

        if self.addon.getSetting('state_state_local_db') == 'true':
            ret = True
        return ret
