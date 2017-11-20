from myjson import MyJson
from addon import Addon


class Data:
    def __init__(self):
        self.ad = Addon()
        self.js = MyJson()

        if self.ad.get_state_local_db():
            self.tdata = self.js.read_json(self.ad.db_file)
        else:
            self.tdata = self.js.get_json("https://github.com/SLiX69/script.skip.intro/raw/master/resources/data.json")
            
