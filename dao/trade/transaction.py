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

    def get_transactions_by_create_time_periods(self, create_time_periods):
        matcher = {
            "create_time_sec": {
                "$gt": str(create_time_periods[0]),
                "$lt": str(create_time_periods[1])
            }
        }
        transactions = self.find_many(matcher)
        return self.PH.batch_to_obj(transactions, transaction_pb.Transaction)
