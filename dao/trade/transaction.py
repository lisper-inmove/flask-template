import proto.trade.transaction_pb2 as transaction_pb
from dao.mongodb import MongoDBHelper


class TransactionDA(MongoDBHelper):

    coll = "___trade_db___transactions___"

    def add_or_update_transaction(self, transaction):
        matcher = {"id": transaction.id}
        json_data = self.PH.to_json(transaction)
        self.update_one(matcher, json_data, upsert=True)

    def get_transaction_by_id(self, id):
        matcher = {"id": id}
        return self.find_one(matcher, transaction_pb.Transaction)
