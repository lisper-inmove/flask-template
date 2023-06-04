import time
from datetime import datetime

import proto.trade.transaction_pb2 as transaction_pb
import api.trade_api_pb2 as trade_api_pb
from ctrl.hctrl.trade.transaction import TransactionCtrl
from manager.trade.transaction import TransactionManager
from manager.user.recharge_record import RechargeRecordManager
from submodules.utils.idate import IDate
from submodules.utils.logger import Logger

logger = Logger()


class TradeChecker:

    fmt = '%Y-%m-%d %H:%M:%S'

    def query(self):
        manager = TransactionManager()
        end_timestamp = IDate.now_timestamp()
        start_timestamp = end_timestamp - IDate.ONE_MIN * 5
        start_time_str = datetime.fromtimestamp(start_timestamp).strftime(self.fmt)
        end_time_str = datetime.fromtimestamp(end_timestamp).strftime(self.fmt)
        logger.info(f"查询 {start_time_str} ~ {end_time_str} 的订单")
        transactions = manager.list_transactions_by_create_time_periods((start_timestamp, end_timestamp))
        for transaction in transactions:
            if transaction.status == transaction_pb.Transaction.SUCCEED:
                continue
            self.__deal_transaction(transaction)

    def __deal_transaction(self, transaction):
        create_time = datetime.fromtimestamp(transaction.create_time_sec).strftime(self.fmt)
        success_time = datetime.fromtimestamp(transaction.success_time).strftime(self.fmt)
        status = transaction_pb.Transaction.Status.Name(transaction.status)
        logger.info(f"订单: {transaction.id} {create_time} {success_time} {status}")
        ctrl = TransactionCtrl()
        req = trade_api_pb.QueryRequest()
        req.transaction_id = transaction.id
        result = ctrl.query(req)
        logger.info(f"订单支付状态: {result.success} {result.msg} {result.sub_msg}")
        if not result.success:
            return
        self.__set_chatbot_plus_pay_success(transaction)

    def __set_chatbot_plus_pay_success(self, transaction):
        if transaction.type != transaction_pb.Transaction.CHATBOT_PLUS:
            return
        manager = RechargeRecordManager()
        recharge_record = manager.get_recharge_record_by_id(transaction.order_id)
        if not recharge_record:
            return
        manager.make_recharge_record_success(recharge_record, transaction)
        manager = TransactionManager()
        manager.make_transaction_success(transaction)


if __name__ == '__main__':
    obj = TradeChecker()
    while True:
        obj.query()
        time.sleep(5)
