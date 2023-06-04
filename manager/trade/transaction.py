import proto.trade.transaction_pb2 as transaction_pb
from dao.trade.transaction import TransactionDA
from manager.base_manager import BaseManager
from submodules.utils.idate import IDate


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
        if req.pay_method != "":
            t.pay_method = transaction_pb.Transaction.PayMethod.Value(req.pay_method)
        if req.type != "":
            t.type = transaction_pb.Transaction.Type.Value(req.type)
        return t

    def get_transaction(self, req):
        transaction = self.transaction_da.get_transaction_by_id(req.transaction_id)
        return transaction

    def list_transactions_by_create_time_periods(self, create_time_periods):
        transactions = self.transaction_da.get_transactions_by_create_time_periods(
            create_time_periods)
        return transactions

    def make_transaction_success(self, transaction):
        transaction.status = transaction_pb.Transaction.SUCCEED
        transaction.success_time = IDate.now_timestamp()
        self.add_or_update_transaction(transaction)

    def add_or_update_transaction(self, transaction):
        if not transaction:
            return
        super().update_obj(transaction)
        self.transaction_da.add_or_update_transaction(transaction)
