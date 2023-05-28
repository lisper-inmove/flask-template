import api.trade_api_pb2 as trade_api_pb
from ctrl.base_ctrl import BaseCtrl
from manager.trade.transaction import TransactionManager


class TransactionCtrl(BaseCtrl):

    def prepay(self):
        req = self.get_request_obj(trade_api_pb.PrepayRequest)
        manager = TransactionManager()
        transaction = manager.create_transaction(req)
        result = self.__prepay(transaction)
        manager.add_or_update_transaction(transaction)
        return result

    def __prepay(self, transaction):
        return self.__alipay_prepay(transaction)

    def __alipay_prepay(self, transaction):
        pass
