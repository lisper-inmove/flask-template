import api.trade_api_pb2 as trade_api_pb
import proto.trade.transaction_pb2 as transaction_pb
import proto.user.membership_pb2 as membership_pb
from ctrl.base_ctrl import BaseCtrl
from manager.trade.transaction import TransactionManager
from manager.user.recharge_record import RechargeRecordManager
from manager.user.recharge_config import RechargeConfigManager
from submodules.payment.proxy import PaymentProxy
from submodules.utils.jwt_util import JWTUtil
from view.errors import PopupError


class TransactionCtrl(BaseCtrl):

    @property
    def transaction_manager(self):
        if self._transaction_manager is None:
            self._transaction_manager = TransactionManager()
        return self._transaction_manager

    def _init(self, *args, **kargs):
        self._transaction_manager = None

    def list(self):
        req = self.get_request_obj(trade_api_pb.ListTransactionRequest)
        transactions = self.transaction_manager.list_transactions(req)
        count = self.transaction_manager.count()
        resp = self.__convert_transaction_to_QueryTransactionResponses(transactions)
        resp.count = count
        return resp

    def list_by_status(self):
        req = self.get_request_obj(trade_api_pb.ListTransactionRequest)
        status_map = {v: k for k, v in
                      self.transaction_manager.STATUS_MAP.items()}
        if req.status == '':
            return self.list()
        req.status = status_map.get(req.status)
        transactions = self.transaction_manager.list_transaction_by_status(req)
        count = self.transaction_manager.count_by_status(req.status)
        resp = self.__convert_transaction_to_QueryTransactionResponses(transactions)
        resp.count = count
        return resp

    def __convert_transaction_to_QueryTransactionResponse(self, transaction):
        resp = trade_api_pb.QueryTransactionResponse()
        resp.id = transaction.id
        resp.status = transaction_pb.Transaction.Status.Name(transaction.status)
        resp.status = self.transaction_manager.STATUS_MAP.get(resp.status)
        resp.pay_method = transaction_pb.Transaction.PayMethod.Name(transaction.pay_method)
        resp.pay_method = self.transaction_manager.PAY_METHOD_MAP.get(resp.pay_method)
        resp.type = transaction_pb.Transaction.Type.Name(transaction.type)
        resp.type = self.transaction_manager.TYPE_MAP.get(resp.type)
        resp.create_time = transaction.create_time_sec
        resp.success_time = transaction.success_time
        resp.pay_fee = transaction.pay_fee
        resp.third_party_id = transaction.third_party_id
        return resp

    def __convert_transaction_to_QueryTransactionResponses(self, transactions):
        resp = trade_api_pb.ListTransactionResponse()
        for transaction in transactions:
            resp.transactions.add().CopyFrom(
                self.__convert_transaction_to_QueryTransactionResponse(transaction))
        return resp

    def prepay(self):
        # TODO: 从token中取出用户ID,存入transaction中
        # TODO: 在业务逻辑中将token去除，在网关中处理token
        # TODO: 在Api网关中用token取出userId放到header中
        req = self.get_request_obj(trade_api_pb.PrepayRequest)
        token = self.get_header_param("token")
        decoded_data = JWTUtil().decode(token)
        transaction = self.transaction_manager.create_transaction(req)
        transaction.payer_id = decoded_data.get("id")
        self.__create_order(transaction, req)
        result = self.__prepay(transaction)
        self.transaction_manager.add_or_update_transaction(transaction)
        resp = trade_api_pb.PrepayResponse()
        resp.transaction_id = transaction.id
        resp.qrcode_url = result.qrcode_url
        resp.pay_method = transaction_pb.Transaction.PayMethod.Name(
            transaction.pay_method)
        return resp

    def __create_order(self, transaction, req):
        if transaction.type == transaction_pb.Transaction.CHATBOT_PLUS:
            self.__create_recharge_record(transaction, req)

    def __create_recharge_record(self, transaction, req):
        if transaction.type != transaction_pb.Transaction.CHATBOT_PLUS:
            return
        recharge_config_manager = RechargeConfigManager()
        recharge_config = recharge_config_manager.get_recharge_config_by_id(
            req.commodity_id)
        if not recharge_config:
            raise PopupError(f"{req.commodity_id}商品不存在")
        recharge_record_manager = RechargeRecordManager()
        recharge_record = recharge_record_manager.create_obj(
            membership_pb.RechargeRecord)
        recharge_record.config.CopyFrom(recharge_config)
        transaction.order_id = recharge_record.id
        transaction.pay_fee = recharge_config.price
        recharge_record_manager.add_or_update_recharge_record(recharge_record)

    def notify(self):
        # 暂不用回调
        pass

    def query(self, req=None, transaction=None):
        if req is None:
            req = self.get_request_obj(trade_api_pb.QueryRequest)
        if transaction is None:
            transaction = self.transaction_manager.get_transaction(req)
        result = self.__query(transaction)
        resp = trade_api_pb.QueryResponse()
        resp.transaction_id = transaction.id
        resp.success = result.success
        resp.msg = result.msg
        resp.sub_msg = result.sub_msg
        return resp

    def __prepay(self, transaction):
        obj = PaymentProxy()
        if transaction.pay_method == transaction_pb.Transaction.ALIPAY_F2F:
            result = obj.alipay_f2f_prepay(transaction.id, transaction.pay_fee)
        return result

    def __query(self, transaction):
        obj = PaymentProxy()
        result = None
        if transaction.pay_method == transaction_pb.Transaction.ALIPAY_F2F:
            result = obj.query_alipay_trade(transaction.id)
            if not result.success:
                return result
            transaction.third_party_id = result.third_party_id
        return result
