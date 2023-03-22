import sys
import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

from vnpy.event import EventEngine
from vnpy.trader.constant import (
    Direction,
    Exchange,
    OrderType,
    Offset,
    Product,
    Status,
    OptionType
)
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.utility import round_to, get_folder_path, ZoneInfo
from vnpy.trader.object import (
    TickData,
    OrderData,
    TradeData,
    PositionData,
    AccountData,
    ContractData,
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
)
from vnpy.trader.event import EVENT_TIMER

from ..api.hft import (
    OptionApi,
    AccountType_Options,
    PositionSide_Long,
    PositionSide_Short,
    OrderSide_Buy_Open,
    OrderSide_Buy_Close,
    OrderSide_Sell_Open,
    OrderSide_Sell_Close,
    OrderType_LMT,
    OrderType_B5TC,
    OrderStatus_PendingNew,
    OrderStatus_New,
    OrderStatus_PartiallyFilled,
    OrderStatus_Filled,
    OrderStatus_PendingCancel,
    OrderStatus_Canceling,
    OrderStatus_CancelFilled,
    OrderStatus_PartiallyCanceled,
    OrderStatus_Rejected,
    OrderStatus_CancelRejected,
    TradeReportType_Normal,
    OrderFlag_Future_Option_Speculation
)
from ..api.sip import (
    MdApi,
    MKtype_SHOP,
    MKtype_SZOP,
)
from .terminal_info import get_terminal_info


# 市场映射
MK_HFT2VT: Dict[int, Exchange] = {
    MKtype_SHOP: Exchange.SSE,
    MKtype_SZOP: Exchange.SZSE

}
MK_VT2HFT: Dict[Exchange, int] = {v: k for k, v in MK_HFT2VT.items()}

# 产品类型映射
SH_PRODUCT_HFT2VT: Dict[str, Product] = {
    "ES": Product.EQUITY,
    "D": Product.BOND,
    "RWS": Product.OPTION,
    "FF": Product.FUTURES,
    "EU": Product.FUND
}
SZ_PRODUCT_HFT2VT: Dict[int, Product] = {
    1: Product.EQUITY,
    2: Product.EQUITY,
    3: Product.EQUITY,
    4: Product.EQUITY,
    5: Product.BOND,
    6: Product.BOND,
    7: Product.BOND,
    8: Product.BOND,
    9: Product.BOND,
    10: Product.BOND,
    11: Product.BOND,
    12: Product.BOND,
    13: Product.BOND,
    14: Product.ETF,
    15: Product.ETF,
    16: Product.ETF,
    17: Product.ETF,
    18: Product.ETF,
    19: Product.ETF,
    20: Product.ETF,
    21: Product.ETF,
    22: Product.ETF,
    23: Product.FUND,
    24: Product.FUND,
    25: Product.FUND,
    26: Product.FUND,
    28: Product.OPTION,
    29: Product.OPTION,
    30: Product.OPTION,
    33: Product.EQUITY,
    34: Product.BOND,
    35: Product.BOND,

}

# 委托类型映射
ORDERSTATUS_HFT2VT: Dict[int, Status] = {
    OrderStatus_PendingNew: Status.SUBMITTING,
    OrderStatus_New: Status.NOTTRADED,
    OrderStatus_PartiallyFilled: Status.PARTTRADED,
    OrderStatus_Filled: Status.ALLTRADED,
    OrderStatus_PendingCancel: Status.SUBMITTING,
    OrderStatus_Canceling: Status.CANCELLED,
    OrderStatus_CancelFilled: Status.CANCELLED,
    OrderStatus_PartiallyCanceled: Status.CANCELLED,
    OrderStatus_Rejected: Status.REJECTED,
    OrderStatus_CancelRejected: Status.REJECTED,
}
ORDERTYPE_HFT2VT: Dict[int, OrderType] = {
    OrderType_LMT: OrderType.LIMIT,
    OrderType_B5TC: OrderType.MARKET
}
ORDERTYPE_VT2HFT: Dict[OrderType, int] = {
    v: k for k, v in ORDERTYPE_HFT2VT.items()
}

# 交易所映射
EXCHANGE_HFT2VT: Dict[str, Exchange] = {
    "SHOP": Exchange.SSE,
    "SZOP": Exchange.SZSE
}
EXCHANGE_VT2HFT: Dict[Exchange, str] = {
    v: k for k, v in EXCHANGE_HFT2VT.items()
}

# 多空方向映射
DIRECTION_HFT2VT: Dict[int, Any] = {
    PositionSide_Long: Direction.LONG,
    PositionSide_Short: Direction.SHORT,
}
SIDE_HFT2VT: Dict[int, tuple] = {
    OrderSide_Buy_Open: (Direction.LONG, Offset.OPEN),
    OrderSide_Buy_Close: (Direction.LONG, Offset.CLOSE),
    OrderSide_Sell_Open: (Direction.SHORT, Offset.OPEN),
    OrderSide_Sell_Close: (Direction.SHORT, Offset.CLOSE),
}
SIDE_VT2HFT: Dict[Any, int] = {
    v: k for k, v in SIDE_HFT2VT.items()
}

# 期权类型映射
OPTIONTYPE_HFT2VT: Dict[str, OptionType] = {
    "C": OptionType.CALL,
    "P": OptionType.PUT
}

# 其他常量
MAX_FLOAT = sys.float_info.max                  # 浮点数极限值
CHINA_TZ = ZoneInfo("Asia/Shanghai")            # 中国时区

# 合约数据全局缓存字典
symbol_contract_map: Dict[str, ContractData] = {}


class HftOptionGateway(BaseGateway):
    """
    VeighNa用于对接国泰君安期权的交易接口。
    """

    default_name: str = "HFTOPTION"

    default_setting: Dict[str, str] = {
        "交易用户名": "",
        "交易密码": "",
        "交易服务器": "",
        "交易端口": "",
        "机构代号": "",
        "营业部代号": "",
        "网关": "",
        "行情用户名": "",
        "行情密码": "",
        "行情服务器": "",
        "行情端口": ""
    }

    exchanges: List[str] = [Exchange.SSE, Exchange.SZSE]

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        """构造函数"""
        super().__init__(event_engine, gateway_name)

        self.td_api: "HftTdApi" = HftTdApi(self)
        self.md_api: "HftMdApi" = HftMdApi(self)

    def connect(self, setting: dict) -> None:
        """连接交易接口"""
        td_userid: str = setting["交易用户名"]
        td_password: str = setting["交易密码"]
        td_ip: str = setting["交易服务器"]
        td_port: str = setting["交易端口"]
        orgid: str = setting["机构代号"]
        barnchid: str = setting["营业部代号"]
        system_id: str = setting["网关"]

        md_userid: str = setting["行情用户名"]
        md_password: str = setting["行情密码"]
        md_ip: str = setting["行情服务器"]
        md_port: str = setting["行情端口"]

        self.td_api.connect(
            td_userid,
            td_password,
            orgid,
            barnchid,
            system_id,
            td_ip,
            td_port
        )

        self.md_api.connect(
            md_ip,
            md_port,
            md_userid,
            md_password,
        )

    def subscribe(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        self.md_api.subscrbie(req)

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        self.td_api.send_order(req)

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
        self.td_api.cancel_order(req)

    def query_account(self) -> None:
        """查询资金"""
        self.td_api.query_account()

    def query_position(self):
        """查询持仓"""
        self.td_api.query_position()

    def close(self) -> None:
        """关闭接口"""
        self.td_api.close()
        self.md_api.close()

    def write_error(self, msg: str, error: dict) -> None:
        """输出错误信息日志"""
        error_id: int = error["err_code"]
        error_msg: str = error["err_msg"]
        msg: str = f"{msg}，代码：{error_id}，信息：{error_msg}"
        self.write_log(msg)

    def process_timer_event(self, event) -> None:
        """定时事件处理"""
        self.count += 1
        if self.count < 2:
            return
        self.count = 0

        func = self.query_functions.pop(0)
        func()
        self.query_functions.append(func)

    def init_query(self) -> None:
        """初始化查询任务"""
        self.count: int = 0
        self.query_functions: list = [self.query_account, self.query_position]
        self.event_engine.register(EVENT_TIMER, self.process_timer_event)


class HftMdApi(MdApi):

    def __init__(self, gateway: HftOptionGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: HftOptionGateway = gateway
        self.gateway_name: str = gateway.gateway_name

        self.userid: str = ""
        self.password: str = ""
        self.client_id: int = 0
        self.server_ip: str = ""
        self.server_port: int = 0
        self.protocol: int = 0
        self.session_id: int = 0
        self.date: str = ""

        self.connect_status: bool = False
        self.login_status: bool = False

        self.sse_inited: bool = False
        self.szse_inited: bool = False

    def onDisconnected(self, reason: int) -> None:
        """服务器连接断开回报"""
        self.connect_status = False
        self.login_status = False
        self.gateway.write_log(f"行情服务器连接断开, 原因{reason}")

        self.login()

    def onSubscribe(self, error) -> None:
        """订阅行情回报"""
        if error["errcode"]:
            self.gateway.write_log(
                f"订阅失败，错误码{error['errcode']}，信息{error['errstr']}"
            )

    def onMarketData(self, mk_type: int, symbol: str, data: dict) -> None:
        """行情数据推送"""
        print("onMarketData")
        timestamp: str = f"{self.date} {str(data['nTime'])}"
        dt: datetime = generate_datetime(timestamp)

        tick: TickData = TickData(
            symbol=symbol,
            exchange=MK_HFT2VT[mk_type],
            datetime=dt,
            volume=data["iVolume"],
            last_price=data["uMatch"] / 10000,
            limit_up=data["uHighLimited"] / 10000,
            limit_down=data["uLowLimited"] / 10000,
            open_price=data["uOpen"] / 10000,
            high_price=data["uHigh"] / 10000,
            low_price=data["uLow"] / 10000,
            pre_close=data["uPreClose"] / 10000,
            gateway_name=self.gateway_name
        )
        contract: ContractData = symbol_contract_map[tick.symbol]

        tick.bid_price_1, tick.bid_price_2, tick.bid_price_3, tick.bid_price_4, tick.bid_price_5 = data["bid"][0:5]
        tick.ask_price_1, tick.ask_price_2, tick.ask_price_3, tick.ask_price_4, tick.ask_price_5 = data["ask"][0:5]
        tick.bid_volume_1, tick.bid_volume_2, tick.bid_volume_3, tick.bid_volume_4, tick.bid_volume_5 = data["bid_qty"][0:5]
        tick.ask_volume_1, tick.ask_volume_2, tick.ask_volume_3, tick.ask_volume_4, tick.ask_volume_5 = data["ask_qty"][0:5]

        pricetick: float = contract.pricetick
        if pricetick:
            tick.bid_price_1 = round_to(tick.bid_price_1 / 10000, pricetick)
            tick.bid_price_2 = round_to(tick.bid_price_2 / 10000, pricetick)
            tick.bid_price_3 = round_to(tick.bid_price_3 / 10000, pricetick)
            tick.bid_price_4 = round_to(tick.bid_price_4 / 10000, pricetick)
            tick.bid_price_5 = round_to(tick.bid_price_5 / 10000, pricetick)
            tick.ask_price_1 = round_to(tick.ask_price_1 / 10000, pricetick)
            tick.ask_price_2 = round_to(tick.ask_price_2 / 10000, pricetick)
            tick.ask_price_3 = round_to(tick.ask_price_3 / 10000, pricetick)
            tick.ask_price_4 = round_to(tick.ask_price_4 / 10000, pricetick)
            tick.ask_price_5 = round_to(tick.ask_price_5 / 10000, pricetick)

        tick.name = contract.name
        self.gateway.on_tick(tick)

    def onSHOption(self, code: str, data: dict) -> None:
        """上交所期权快照行情数据回调"""
        # print("OnSHOption")
        timestamp: str = f"{self.date} {str(data['nTime'])}"
        dt: datetime = generate_datetime(timestamp)

        tick: TickData = TickData(
            symbol=code,
            exchange=Exchange.SSE,
            datetime=dt,
            volume=data["iTotalVolumeTrade"],
            last_price=data["iLastPx"],
            limit_up=data["iDailyPriceUpLimit"],
            limit_down=data["iDailyPriceDownLimit"],
            open_price=data["iOpenPx"] / 10000,
            high_price=data["iHighPx"] / 10000,
            low_price=data["iLowPx"] / 10000,
            pre_close=data["iPreSettlPrice"] / 10000,
            gateway_name=self.gateway_name
        )
        contract: ContractData = symbol_contract_map[tick.symbol]

        tick.bid_price_1, tick.bid_price_2, tick.bid_price_3, tick.bid_price_4, tick.bid_price_5 = data["bid"][0:5]
        tick.ask_price_1, tick.ask_price_2, tick.ask_price_3, tick.ask_price_4, tick.ask_price_5 = data["ask"][0:5]
        tick.bid_volume_1, tick.bid_volume_2, tick.bid_volume_3, tick.bid_volume_4, tick.bid_volume_5 = data["bid_qty"][0:5]
        tick.ask_volume_1, tick.ask_volume_2, tick.ask_volume_3, tick.ask_volume_4, tick.ask_volume_5 = data["ask_qty"][0:5]

        pricetick: float = contract.pricetick
        if pricetick:
            tick.bid_price_1 = round_to(tick.bid_price_1 / 10000, pricetick)
            tick.bid_price_2 = round_to(tick.bid_price_2 / 10000, pricetick)
            tick.bid_price_3 = round_to(tick.bid_price_3 / 10000, pricetick)
            tick.bid_price_4 = round_to(tick.bid_price_4 / 10000, pricetick)
            tick.bid_price_5 = round_to(tick.bid_price_5 / 10000, pricetick)
            tick.ask_price_1 = round_to(tick.ask_price_1 / 10000, pricetick)
            tick.ask_price_2 = round_to(tick.ask_price_2 / 10000, pricetick)
            tick.ask_price_3 = round_to(tick.ask_price_3 / 10000, pricetick)
            tick.ask_price_4 = round_to(tick.ask_price_4 / 10000, pricetick)
            tick.ask_price_5 = round_to(tick.ask_price_5 / 10000, pricetick)

        tick.name = contract.name
        self.gateway.on_tick(tick)

    def onSZOption(self, code: str, data: dict) -> None:
        """深交所期权快照行情数据回调"""
        timestamp: str = f"{self.date} {str(data['nTime'])}"
        dt: datetime = generate_datetime(timestamp)

        tick: TickData = TickData(
            symbol=code,
            exchange=Exchange.SSE,
            datetime=dt,
            volume=data["i64TotalVolumeTrade"],
            last_price=data["i64LastPrice"],
            limit_up=data["i64PriceUpperLimit"],
            limit_down=data["i64PriceLowerLimit"],
            open_price=data["i64OpenPrice"] / 10000,
            high_price=data["i64HighPrice"] / 10000,
            low_price=data["i64LowPrice"] / 10000,
            pre_close=data["i64PrevClosePx"] / 10000,
            gateway_name=self.gateway_name
        )
        contract: ContractData = symbol_contract_map[tick.symbol]

        tick.bid_price_1, tick.bid_price_2, tick.bid_price_3, tick.bid_price_4, tick.bid_price_5 = data["bid"][0:5]
        tick.ask_price_1, tick.ask_price_2, tick.ask_price_3, tick.ask_price_4, tick.ask_price_5 = data["ask"][0:5]
        tick.bid_volume_1, tick.bid_volume_2, tick.bid_volume_3, tick.bid_volume_4, tick.bid_volume_5 = data["bid_qty"][0:5]
        tick.ask_volume_1, tick.ask_volume_2, tick.ask_volume_3, tick.ask_volume_4, tick.ask_volume_5 = data["ask_qty"][0:5]

        pricetick: float = contract.pricetick
        if pricetick:
            tick.bid_price_1 = round_to(tick.bid_price_1 / 10000, pricetick)
            tick.bid_price_2 = round_to(tick.bid_price_2 / 10000, pricetick)
            tick.bid_price_3 = round_to(tick.bid_price_3 / 10000, pricetick)
            tick.bid_price_4 = round_to(tick.bid_price_4 / 10000, pricetick)
            tick.bid_price_5 = round_to(tick.bid_price_5 / 10000, pricetick)
            tick.ask_price_1 = round_to(tick.ask_price_1 / 10000, pricetick)
            tick.ask_price_2 = round_to(tick.ask_price_2 / 10000, pricetick)
            tick.ask_price_3 = round_to(tick.ask_price_3 / 10000, pricetick)
            tick.ask_price_4 = round_to(tick.ask_price_4 / 10000, pricetick)
            tick.ask_price_5 = round_to(tick.ask_price_5 / 10000, pricetick)

        tick.name = contract.name
        self.gateway.on_tick(tick)

    def connect(
        self,
        ip: str,
        port: int,
        username: str,
        password: str,
    ) -> None:
        """连接服务器"""
        cfg: str = generate_cfg(ip, port, username, password)

        self.date = datetime.now().strftime("%Y%m%d")

        if not self.connect_status:
            self.initialize(cfg, False)
            n: int = self.login()
            self.query_contract()

            if not n:
                self.gateway.write_log("行情服务器登录成功")
                self.connect_status = True
                self.login_status = True
            else:
                self.gateway.write_log(f"行情登录失败，错误号{n}")
        else:
            self.gateway.write_log("行情接口已登录，请勿重复操作")

    def close(self) -> None:
        """关闭连接"""
        pass

    def subscrbie(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        if self.login_status:
            exchange = MK_VT2HFT.get(req.exchange, "")
            self.subscribeMarketData(exchange, req.symbol)

    def query_contract(self) -> None:
        """查询合约"""
        # 8 -> 上交所期权
        # 11 -> 深交所期权
        self.subscribeBaseInfo(8)
        self.subscribeBaseInfo(11)

    def onSHOptionBaseInfo(self, code: str, data: dict) -> None:
        """上交所期权合约查询回报"""
        # print("onSHOptionBaseInfo", data)
        contract: ContractData = ContractData(
            gateway_name=self.gateway_name,
            symbol=code,
            exchange=Exchange.SSE,
            name=data["sContractSymbol"],
            product=Product.OPTION,
            pricetick=data["uTickSize"],
            size=data["uRoundLot"]
        )
        contract.option_underlying = (
            data["sUnderlyingSecurityID"]
            + "-"
            + data["sExpireDate"]
        )
        contract.option_portfolio = data["sUnderlyingSecurityID"] + "_O"
        contract.option_type = OPTIONTYPE_HFT2VT[data["cCallOrPut"]]
        contract.option_strike = data["uExercisePrice"]
        contract.option_expiry = datetime.strptime(
            data["sExpireDate"], "%Y%m%d"
        )
        contract.option_index = get_option_index(
            contract.option_strike, data["sSecurityID"]
        )

        self.gateway.on_contract(contract)
        symbol_contract_map[contract.symbol] = contract

    def onSZOptionBaseInfo(self, code: str, data: dict) -> None:
        """深交所期权合约查询回报"""
        print("onSZOptionBaseInfo", data)
        contract: ContractData = ContractData(
            gateway_name=self.gateway_name,
            symbol=code,
            exchange=Exchange.SZSE,
            name=data["sSymbol"],
            product=Product.OPTION,
            pricetick=data["i64PriceTick"],
            size=data["i64ContractUnit"]
        )
        contract.option_underlying = (
            data["sUnderlyingSecurityID"]
            + "-"
            + str(data["nDeliveryDay"])
        )
        contract.option_portfolio = data["sUnderlyingSecurityID"] + "_O"
        contract.option_type = OPTIONTYPE_HFT2VT[data["cCallOrPut"]]
        contract.option_strike = data["i64ExercisePrice"]
        contract.option_expiry = datetime.strptime(
            str(data["nDeliveryDay"]), "%Y%m%d"
        )
        contract.option_index = get_option_index(
            contract.option_strike, data["sSecurityID"]
        )

        self.gateway.on_contract(contract)
        symbol_contract_map[contract.symbol] = contract


class HftTdApi(OptionApi):
    """"""

    def __init__(self, gateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: HftOptionGateway = gateway
        self.gateway_name: str = gateway.gateway_name

        self.reqid: int = 0
        self.order_count: int = 0

        self.connect_status: bool = False
        self.login_status: bool = False

        self.userid: str = ""
        self.password: str = ""
        self.orders: Dict[str, OrderData] = {}
        self.short_positions: Dict[str, PositionData] = {}

        self.orderid_sysid_map: Dict[str, str] = {}

        self.prefix: str = ""

    def onError(self, error: dict, reqid: int) -> None:
        """错误回报"""
        self.gateway.write_error("错误", error)

    def onRiskNotify(self, data: dict) -> None:
        """风险警告回报"""
        status: str = data["alarm_status"]
        rule: str = data["alarm_rule"]
        self.gateway.write_log(f"触发风险警告，状态{status}，类型{rule}")

    def onDisconnect(self) -> None:
        """服务器连接断开回报"""
        self.login_status = False
        self.gateway.write_log("交易服务器连接断开")

    def onLogin(self, data: dict, error: dict) -> None:
        """用户登录请求回报"""
        if not error["err_code"]:
            self.login_status = True
            self.gateway.write_log("交易服务器登录成功")

            self.query_order()
            self.query_trade()
            self.gateway.init_query()
        else:
            self.gateway.write_error("交易服务器登录失败", error)

    def onOrderStatus(self, data) -> None:
        """委托更新推送"""
        exchange, symbol = data["symbol"].split(".")

        orderid: str = data["cl_order_id"]
        sysid: str = data["order_id"]
        if not orderid:
            orderid = sysid

        timestamp: str = f"{data['order_date']} {data['order_time']}"
        dt: datetime = generate_datetime(timestamp)

        direction, offset = SIDE_HFT2VT[data["side"]]

        order: OrderData = self.orders.get(orderid, None)
        if not order:
            order = OrderData(
                orderid=orderid,
                gateway_name=self.gateway_name,
                symbol=symbol,
                exchange=EXCHANGE_HFT2VT[exchange],
                direction=direction,
                offset=offset,
                type=ORDERTYPE_HFT2VT.get(data["order_type"], OrderType.MARKET),
                price=data["price"] / 10000,
                volume=data["volume"],
                traded=data["filled_volume"],
                status=ORDERSTATUS_HFT2VT[data["order_status"]],
                datetime=dt,
            )
            self.orders[orderid] = order
        elif not order.datetime:
            order.datetime = dt

        order.traded = data["filled_volume"]
        order.status = ORDERSTATUS_HFT2VT[data["order_status"]]

        self.gateway.on_order(order)

    def onTradeReport(self, data) -> None:
        """成交数据推送"""
        exchange, symbol = data["symbol"].split(".")

        orderid: str = data["cl_order_id"]
        sysid: str = data["order_id"]
        if not orderid:
            orderid = sysid

        timestamp: str = f"{data['trade_date']} {data['trade_time']}"
        dt: datetime = generate_datetime(timestamp)

        direction, offset = SIDE_HFT2VT[data["side"]]

        if data["report_type"] == TradeReportType_Normal:
            trade: TradeData = TradeData(
                tradeid=data["report_no"],
                orderid=orderid,
                gateway_name=self.gateway_name,
                symbol=symbol,
                exchange=EXCHANGE_HFT2VT[exchange],
                direction=direction,
                offset=offset,
                price=data["price"] / 10000,
                volume=data["volume"],
                datetime=dt,
            )
            self.gateway.on_trade(trade)

    def onOrderRsp(
        self,
        data: dict,
        error: dict,
        reqid: int,
        last: bool
    ):
        """委托下单回报"""
        orderid: str = data["cl_order_id"]
        order: OrderData = self.orders[orderid]

        if error["err_code"]:
            self.gateway.write_error("交易委托失败", error)

            order.status = Status.REJECTED
            dt: datetime = datetime.now()
            dt: datetime = dt.replace(tzinfo=CHINA_TZ)
            order.datetime = dt
            self.gateway.on_order(order)
        else:
            sysid: str = data["order_id"]
            self.orderid_sysid_map[orderid] = sysid

    def onCancelRsp(
        self,
        data: dict,
        error: dict,
        reqid: int,
        last: bool
    ) -> None:
        """委托撤单失败回报"""
        if error["err_code"]:
            self.gateway.write_error("交易撤单失败", error)

    def onQueryPositionRsp(
        self,
        data: dict,
        error: dict,
        reqid: int,
        last: bool
    ) -> None:
        """持仓查询回报"""
        if not data["symbol"]:
            return

        exchange, symbol = data["symbol"].split(".")

        pos: PositionData = PositionData(
            gateway_name=self.gateway_name,
            symbol=symbol,
            exchange=EXCHANGE_HFT2VT[exchange],
            direction=DIRECTION_HFT2VT[data["side"]],
            volume=data["volume"],
            price=data["buy_cost"] / data["volume"],
        )
        self.gateway.on_position(pos)

    def onQueryCashRsp(self, data: dict, error: dict, reqid: int) -> None:
        """资金查询回报"""
        account: AccountData = AccountData(
            accountid=data["account_id"],
            balance=data["total_amount"] / 10000,
            frozen=(data["total_amount"] - data["avail_amount"]) / 10000,
            gateway_name=self.gateway_name
        )
        self.gateway.on_account(account)

    def onQueryOrderRsp(
        self,
        data: dict,
        error: dict,
        reqid: int,
        last: bool,
        pos: str
    ) -> None:
        """未成交委托查询回报"""
        if not error["err_code"]:
            exchange, symbol = data["symbol"].split(".")

            orderid: str = data["cl_order_id"]
            sysid: str = data["order_id"]
            if not orderid:
                orderid = sysid
            else:
                self.orderid_sysid_map[orderid] = sysid

            timestamp: str = f"{data['order_date']} {data['order_time']}"
            dt: datetime = generate_datetime(timestamp)

            direction, offset = SIDE_HFT2VT[data["side"]]

            order: OrderData = OrderData(
                orderid=orderid,
                gateway_name=self.gateway_name,
                symbol=symbol,
                exchange=EXCHANGE_HFT2VT[exchange],
                direction=direction,
                offset=offset,
                type=ORDERTYPE_HFT2VT.get(data["order_type"], OrderType.MARKET),
                price=data["price"] / 10000,
                volume=data["volume"],
                status=ORDERSTATUS_HFT2VT[data["order_status"]],
                traded=data["filled_volume"],
                datetime=dt,
            )
            self.orders[orderid] = order
            self.gateway.on_order(order)

            if last:
                self.query_order(pos)

        elif error["err_code"] != 14020:
            self.gateway.write_error(error)

        else:
            self.gateway.write_log("查询委托信息成功")

    def onQueryTradeRsp(
        self,
        data: dict,
        error: dict,
        reqid: int,
        last: bool,
        pos: str
    ) -> None:
        """成交信息查询回报"""
        if not error["err_code"]:
            exchange, symbol = data["symbol"].split(".")

            orderid: str = data["cl_order_id"]
            sysid: str = data["order_id"]
            if not orderid:
                orderid = sysid

            timestamp: str = f"{data['trade_date']} {data['trade_time']}"
            dt: datetime = generate_datetime(timestamp)

            direction, offset = SIDE_HFT2VT[data["side"]]

            trade: TradeData = TradeData(
                tradeid=data["report_no"],
                orderid=orderid,
                gateway_name=self.gateway_name,
                symbol=symbol,
                exchange=EXCHANGE_HFT2VT[exchange],
                direction=direction,
                offset=offset,
                price=data["price"] / 10000,
                volume=data["volume"],
                datetime=dt,
            )
            self.gateway.on_trade(trade)

            if last:
                self.query_trade(pos)

        elif error["err_code"] != 14020:
            self.gateway.write_error(error)

        else:
            self.gateway.write_log("查询成交信息成功")

    def connect(
        self,
        userid: str,
        password: str,
        orgid: str,
        branchid: str,
        system_id: str,
        host: str,
        port: str,
    ) -> None:
        """连接服务器"""
        self.userid = userid
        self.password = password
        self.prefix = datetime.now().strftime("%Y%m%d%H%M%S")

        if not self.connect_status:
            path: Path = get_folder_path(self.gateway_name.lower())
            self.setLogConfig(str(path).encode("GBK"))
            self.createTraderApi()

            account_info: dict = {
                "account_id": userid,
                "account_type": AccountType_Options,
                "account_pwd": password,
                "cust_orgid": orgid,
                "cust_branchid": branchid,
                "cl_system_id": system_id,
                "svr_ip": host,
                "svr_port": int(port),
                "terminal_info": get_terminal_info()
            }
            self.login(account_info)

            self.connect_status = True

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        if req.type not in ORDERTYPE_VT2HFT:
            self.gateway.write_log(f"当前接口不支持该类型的委托{req.type.value}")
            return ""

        if req.offset == Offset.NONE:
            self.gateway.write_log("委托失败，需要选择开平方向")
            return ""

        self.order_count += 1
        suffix: str = str(self.order_count).rjust(6, "0")
        orderid: str = f"{self.prefix}_{suffix}"

        exchange: Exchange = EXCHANGE_VT2HFT[req.exchange]
        hft_symbol: str = f"{exchange}.{req.symbol}"

        order_req: dict = {
            "cl_order_id": orderid,
            "symbol": hft_symbol,
            "order_type": ORDERTYPE_VT2HFT[req.type],
            "volume": int(req.volume),
            "price": int(req.price * 10000),
            "side": SIDE_VT2HFT[(req.direction, req.offset)],
            "order_flag": OrderFlag_Future_Option_Speculation
        }

        self.reqid += 1
        self.order(order_req, self.reqid)

        order: OrderData = req.create_order_data(orderid, self.gateway_name)
        self.orders[orderid] = order
        self.gateway.on_order(order)
        return order.vt_orderid

    def query_order(self, pos_str: str = "") -> None:
        """查询未成交委托"""
        hft_req: dict = {
            "pos_str": pos_str,
            "query_num": 500
        }

        self.reqid += 1
        self.queryOrders(hft_req, self.reqid)

    def query_trade(self, pos_str: str = "") -> None:
        """查询成交"""
        hft_req: dict = {
            "pos_str": pos_str,
            "query_num": 500
        }

        self.reqid += 1
        self.queryTrades(hft_req, self.reqid)

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
        self.reqid += 1
        sysid: str = self.orderid_sysid_map.get(req.orderid, req.orderid)

        cancel_req: dict = {"order_id": sysid}
        self.cancelOrder(cancel_req, self.reqid)

    def query_account(self) -> None:
        """查询资金"""
        self.reqid += 1
        self.queryCash({}, self.reqid)

    def query_position(self) -> None:
        """查询持仓"""
        hft_req: dict = {
            "pos_str": "",
            "query_num": 500
        }

        self.reqid += 1
        self.queryPositions(hft_req, self.reqid)

    def close(self) -> None:
        """关闭连接"""
        if self.connect_status:
            self.exit()


def generate_datetime(timestamp: str) -> datetime:
    """生成时间"""
    dt: datetime = datetime.strptime(timestamp, "%Y%m%d %H%M%S%f")
    dt: datetime = dt.replace(tzinfo=CHINA_TZ)
    return dt


def generate_cfg(ip: str, port: int, username: str, password: str) -> str:
    """生成配置信息"""
    setting: dict = {
        "ip0": ip,
        "port0": port,
        "connect_mode": "NR",
        "username": username,
        "password": password
    }
    cfg: str = json.dumps(setting, separators=("|", ":"))
    return cfg


def get_option_index(strike_price: float, exchange_instrument_id: str) -> str:
    """获取期权索引"""
    exchange_instrument_id: str = exchange_instrument_id.replace(" ", "")

    if "M" in exchange_instrument_id:
        n: int = exchange_instrument_id.index("M")
    elif "A" in exchange_instrument_id:
        n: int = exchange_instrument_id.index("A")
    elif "B" in exchange_instrument_id:
        n: int = exchange_instrument_id.index("B")
    else:
        return str(strike_price)

    index: str = exchange_instrument_id[n:]
    option_index: str = f"{strike_price:.3f}-{index}"

    return option_index