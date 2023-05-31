from dao.mongodb import MongoDBHelper


class ConfigDA(MongoDBHelper):

    coll = "___config_db___configs___"

    def add_or_update_config(self, obj, config):
        matcher = {"id": obj.id}
        json_data = self.PH.to_json(obj)
        json_data.update({"config": config})
        self.update_one(matcher, json_data, upsert=True)

    def get_config_by_application_id(self, application_id):
        matcher = {"application_id": application_id}
        return self._coll.find_one(matcher, {"_id": 0})
