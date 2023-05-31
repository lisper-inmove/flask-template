import api.trade_api_pb2 as trade_api_pb
import proto.trade.transaction_pb2 as transaction_pb
from ctrl.base_ctrl import BaseCtrl
from manager.trade.transaction import TransactionManager
from submodules.payment.proxy import PaymentProxy


class TransactionCtrl(BaseCtrl):

    def prepay(self):
        # TODO: 从token中取出用户ID,存入transaction中
        req = self.get_request_obj(trade_api_pb.PrepayRequest)
        manager = TransactionManager()
        transaction = manager.create_transaction(req)
        result = self.__prepay(transaction)
        manager.add_or_update_transaction(transaction)
        resp = trade_api_pb.PrepayResponse()
        resp.transaction_id = transaction.id
        resp.qrcode_url = result.qrcode_url
        resp.pay_method = transaction_pb.Transaction.PayMethod.Name(
            transaction.pay_method)
        return resp

    def notify(self):
        # 暂不用回调
        pass

    def query(self):
        req = self.get_request_obj(trade_api_pb.QueryRequest)
        manager = TransactionManager()
        transaction = manager.get_transaction(req)
        result = self.__query(transaction)
        manager.add_or_update_transaction(transaction)
        resp = trade_api_pb.QueryResponse()
        resp.transaction_id = transaction.id
        resp.success = result.success
        return resp

    def __prepay(self, transaction):
        obj = PaymentProxy()
        if transaction.pay_method == transaction_pb.Transaction.ALIPAY_F2F:
            result = obj.alipay_f2f_prepay(transaction.id, transaction.pay_fee)
        return result

    def __query(self, transaction):
        obj = PaymentProxy()
        if transaction.pay_method == transaction_pb.Transaction.ALIPAY_F2F:
            result = obj.query_alipay_trade(transaction.id)
            transaction.third_party_id = result.third_party_id
        return result
