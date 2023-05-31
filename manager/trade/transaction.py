import proto.trade.transaction_pb2 as transaction_pb
from dao.trade.transaction import TransactionDA
from manager.base_manager import BaseManager


class TransactionManager(BaseManager):

    @property
    def transaction_da(self):
        if not self._transaction_da:
            self._transaction_da = TransactionDA()
        return self._transaction_da

    def _init(self):
        self._transaction_da = None

    def create_transaction(self, req):
        t = self.create_obj(transaction_pb.Transaction)
        t.pay_fee = req.pay_fee
        t.payer_id = req.payer_id
        t.pay_method = transaction_pb.Transaction.PayMethod.Value(req.pay_method)
        return t

    def get_transaction(self, req):
        transaction = self.transaction_da.get_transaction_by_id(req.transaction_id)
        return transaction

    def add_or_update_transaction(self, transaction):
        self.transaction_da.add_or_update_transaction(transaction)
