import api.recharge_config_api_pb2 as recharge_config_api_pb
from manager.user.recharge_config import RechargeConfigManager
from submodules.utils.idate import IDate


class RechargeConfigHelper:

    def create_recharge_config(self):
        req = recharge_config_api_pb.CreateRechargeConfigRequest()
        name = input("名称: ")
        level = input("等级(默认为GOLD): ")
        price = input("价格(单位: 元): ")
        valid_periods = input("有效时间(默认30天): ")
        if level == "":
            level = "GOLD"
        if valid_periods == "":
            valid_periods = 30
        req.name = name
        req.level = level
        req.price = int(float(price) * 100)
        req.valid_periods = int(int(valid_periods) * IDate.ONE_DAY)
        manager = RechargeConfigManager()
        recharge_config = manager.create_recharge_config(req)
        manager.add_or_update_recharge_config(recharge_config)
        return recharge_config

    def list_recharge_configs(self):
        manager = RechargeConfigManager()
        recharge_configs = manager.list_recharge_configs()
        for index, recharge_config in enumerate(recharge_configs):
            days = recharge_config.valid_periods / IDate.ONE_DAY
            msg = f"""
            第 {index} 条储值配置:
            {recharge_config.id}: {recharge_config.name}
            支付金额: {recharge_config.price / float(100)} 元
            有效时间: {days}天
            """
            print(msg)
        return recharge_configs

    def delete_recharge_config(self):
        recharge_configs = self.list_recharge_configs()
        index = int(input("输入要删除的序号: "))
        recharge_config = recharge_configs[index]
        manager = RechargeConfigManager()
        manager.delete_recharge_config_by_id(recharge_config)


if __name__ == '__main__':
    obj = RechargeConfigHelper()
    jobs = [
        ("新增储值", obj.create_recharge_config),
        ("查询储值列表", obj.list_recharge_configs),
        ("删除", obj.delete_recharge_config),
    ]
    print("有以下可选项: ")
    index = 0
    for name, func in jobs:
        print(f"{index}: {name}")
        index += 1
    select = input("选择要做什么: ")
    select = int(select)
    if select < 0 or select > len(jobs) - 1:
        raise Exception("必须填入 0 ~ {len(jobs) - 1}")
    action = jobs[select][1]()
