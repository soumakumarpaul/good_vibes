from tinydb import TinyDB, Query

class Counters(object):

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.db = self.folder_path + "/counter_db.json"

    def get_count(self, counter_name):
        db = TinyDB(self.db)
        Counter = Query()

        record = db.get(Counter.name == counter_name)
        value = 0
        if record:
            value = record['value'] + 1
            db.update({'value': value}, Counter.name == counter_name)
        else:
            value = 1
            db.insert({'name': counter_name, 'value': value})
        db.close()
        return value