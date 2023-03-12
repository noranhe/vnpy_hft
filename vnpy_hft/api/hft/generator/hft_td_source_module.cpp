.def("login", &TdApi::login)
.def("getCounterType", &TdApi::getCounterType)
.def("getSecuidInfo", &TdApi::getSecuidInfo)
.def("getAllSecuidInfo", &TdApi::getAllSecuidInfo)
.def("getApiLocalAddr", &TdApi::getApiLocalAddr)
.def("order", &TdApi::order)
.def("batchOrder", &TdApi::batchOrder)
.def("cancelOrder", &TdApi::cancelOrder)
.def("batchCancelOrder", &TdApi::batchCancelOrder)
.def("batchCancelAllOrder", &TdApi::batchCancelAllOrder)
.def("queryOrder", &TdApi::queryOrder)
.def("queryOrderByCode", &TdApi::queryOrderByCode)
.def("queryOrders", &TdApi::queryOrders)
.def("queryTradeByOrderId", &TdApi::queryTradeByOrderId)
.def("queryTradeByCode", &TdApi::queryTradeByCode)
.def("queryTrades", &TdApi::queryTrades)
.def("queryETFTrades", &TdApi::queryETFTrades)
.def("queryPosition", &TdApi::queryPosition)
.def("queryPositions", &TdApi::queryPositions)
.def("queryCash", &TdApi::queryCash)
.def("queryJZJYAvailFund", &TdApi::queryJZJYAvailFund)
.def("transferFundInAndOut", &TdApi::transferFundInAndOut)
.def("transferFundBetweenSecuid", &TdApi::transferFundBetweenSecuid)
.def("queryETFs", &TdApi::queryETFs)
.def("queryETFStocks", &TdApi::queryETFStocks)
.def("queryMaxOrderQty", &TdApi::queryMaxOrderQty)
.def("queryIPOMaxPurchase", &TdApi::queryIPOMaxPurchase)
.def("queryIPOStock", &TdApi::queryIPOStock)
.def("querySecurityBaseInfo", &TdApi::querySecurityBaseInfo)
.def("creditMortgageInOut", &TdApi::creditMortgageInOut)
.def("creditStockBack", &TdApi::creditStockBack)
.def("creditPayBack", &TdApi::creditPayBack)
.def("creditPayBackByOrder", &TdApi::creditPayBackByOrder)
.def("queryCreditStock", &TdApi::queryCreditStock)
.def("queryCreditMortgageHold", &TdApi::queryCreditMortgageHold)
.def("queryCreditAssets", &TdApi::queryCreditAssets)
.def("queryCreditFinance", &TdApi::queryCreditFinance)
.def("queryCreditShortsell", &TdApi::queryCreditShortsell)
.def("queryCreditRepayAmount", &TdApi::queryCreditRepayAmount)
.def("queryCreditRepayStock", &TdApi::queryCreditRepayStock)
.def("queryCreditSecuritySellQty", &TdApi::queryCreditSecuritySellQty)
.def("querySecuidRight", &TdApi::querySecuidRight)
.def("queryHKRate", &TdApi::queryHKRate)
.def("queryHKStock", &TdApi::queryHKStock)
.def("queryHKFund", &TdApi::queryHKFund)
.def("queryHKMinPriceUnit", &TdApi::queryHKMinPriceUnit)
.def("queryHKTradeCalendar", &TdApi::queryHKTradeCalendar)
.def("queryLockSecurityDetail", &TdApi::queryLockSecurityDetail)
.def("queryTransferFundHistory", &TdApi::queryTransferFundHistory)
.def("queryCreditDebtsFlow", &TdApi::queryCreditDebtsFlow)
.def("queryCreditAssetFlow", &TdApi::queryCreditAssetFlow)
.def("queryCreditDebts", &TdApi::queryCreditDebts)
.def("doMicroServiceReq", &TdApi::doMicroServiceReq)
.def("queryBankBalance", &TdApi::queryBankBalance)
.def("queryBankInfo", &TdApi::queryBankInfo)
.def("bankSecTransfer", &TdApi::bankSecTransfer)
.def("queryBankSecTransfer", &TdApi::queryBankSecTransfer)
.def("queryHisBankSecTransfer", &TdApi::queryHisBankSecTransfer)
.def("fundAccountTransfer", &TdApi::fundAccountTransfer)
.def("queryFundAccountTransfer", &TdApi::queryFundAccountTransfer)
.def("queryHisOrders", &TdApi::queryHisOrders)
.def("queryHisTrades", &TdApi::queryHisTrades)
.def("queryDeliveryOrders", &TdApi::queryDeliveryOrders)
.def("queryStateOrders", &TdApi::queryStateOrders)
.def("queryExchangeLists", &TdApi::queryExchangeLists)
.def("modifyPassword", &TdApi::modifyPassword)
.def("queryPHXX", &TdApi::queryPHXX)
.def("queryZQXX", &TdApi::queryZQXX)
.def("queryLockSecurityContract", &TdApi::queryLockSecurityContract)
.def("queryCreditContract", &TdApi::queryCreditContract)
.def("queryCreditDebtsCollect", &TdApi::queryCreditDebtsCollect)
.def("queryCreditData", &TdApi::queryCreditData)
.def("queryPreMaturityDebts", &TdApi::queryPreMaturityDebts)
.def("extendPreMaturityDebts", &TdApi::extendPreMaturityDebts)
.def("queryPreMaturityDebtsExtension", &TdApi::queryPreMaturityDebtsExtension)
.def("queryVoteProposal", &TdApi::queryVoteProposal)
.def("queryCreditVoteCount", &TdApi::queryCreditVoteCount)
.def("queryCreditVote", &TdApi::queryCreditVote)
.def("queryNetVoteRights", &TdApi::queryNetVoteRights)
.def("queryNetVoteResult", &TdApi::queryNetVoteResult)
.def("queryNetVoteCount", &TdApi::queryNetVoteCount)
.def("queryStkConcentration", &TdApi::queryStkConcentration)
.def("queryHKHisOrders", &TdApi::queryHKHisOrders)
.def("queryWithdrawCash", &TdApi::queryWithdrawCash)
.def("queryTradeListTotal", &TdApi::queryTradeListTotal)
.def("eTFSubscriptCancel", &TdApi::eTFSubscriptCancel)
.def("queryNetVoteOrder", &TdApi::queryNetVoteOrder)
.def("netVoteOrder", &TdApi::netVoteOrder)
.def("creditNetVoteOrder", &TdApi::creditNetVoteOrder)
.def("queryMSCash", &TdApi::queryMSCash)
.def("queryMSPositions", &TdApi::queryMSPositions)
.def("queryMSCreditDebtsFlow", &TdApi::queryMSCreditDebtsFlow)

.def("onDisconnect", &TdApi::onDisconnect)
.def("onError", &TdApi::onError)
.def("onRiskNotify", &TdApi::onRiskNotify)
.def("onFailBackNotify", &TdApi::onFailBackNotify)
.def("onLogin", &TdApi::onLogin)
.def("onTradeReport", &TdApi::onTradeReport)
.def("onOrderStatus", &TdApi::onOrderStatus)
.def("onOrderRsp", &TdApi::onOrderRsp)
.def("onCancelRsp", &TdApi::onCancelRsp)
.def("onQueryOrderRsp", &TdApi::onQueryOrderRsp)
.def("onQueryTradeRsp", &TdApi::onQueryTradeRsp)
.def("onQueryPositionRsp", &TdApi::onQueryPositionRsp)
.def("onQueryCashRsp", &TdApi::onQueryCashRsp)
.def("onQueryJZJYAvailFundRsp", &TdApi::onQueryJZJYAvailFundRsp)
.def("onTransferFundInAndOutRsp", &TdApi::onTransferFundInAndOutRsp)
.def("onTransferFundBetweenSecuidRsp", &TdApi::onTransferFundBetweenSecuidRsp)
.def("onQueryETFRsp", &TdApi::onQueryETFRsp)
.def("onQueryETFStockRsp", &TdApi::onQueryETFStockRsp)
.def("onQueryMaxOrderQtyRsp", &TdApi::onQueryMaxOrderQtyRsp)
.def("onQueryIPOMaxPurchaseRsp", &TdApi::onQueryIPOMaxPurchaseRsp)
.def("onQueryIPOStockRsp", &TdApi::onQueryIPOStockRsp)
.def("onQuerySecurityBaseInfoRsp", &TdApi::onQuerySecurityBaseInfoRsp)
.def("onCreditMortgageInOutRsp", &TdApi::onCreditMortgageInOutRsp)
.def("onCreditStockBackRsp", &TdApi::onCreditStockBackRsp)
.def("onCreditPayBackRsp", &TdApi::onCreditPayBackRsp)
.def("onCreditPayBackByOrderRsp", &TdApi::onCreditPayBackByOrderRsp)
.def("onQueryCreditStockRsp", &TdApi::onQueryCreditStockRsp)
.def("onQueryCreditMortgageHoldRsp", &TdApi::onQueryCreditMortgageHoldRsp)
.def("onQueryCreditAssetsRsp", &TdApi::onQueryCreditAssetsRsp)
.def("onQueryCreditFinanceRsp", &TdApi::onQueryCreditFinanceRsp)
.def("onQueryCreditShortsellRsp", &TdApi::onQueryCreditShortsellRsp)
.def("onQueryCreditRepayAmountRsp", &TdApi::onQueryCreditRepayAmountRsp)
.def("onQueryCreditRepayStockRsp", &TdApi::onQueryCreditRepayStockRsp)
.def("onQueryCreditSecuritySellQtyRsp", &TdApi::onQueryCreditSecuritySellQtyRsp)
.def("onQuerySecuidRightRsp", &TdApi::onQuerySecuidRightRsp)
.def("onQueryHKRateRsp", &TdApi::onQueryHKRateRsp)
.def("onQueryHKStockRsp", &TdApi::onQueryHKStockRsp)
.def("onQueryHKFundRsp", &TdApi::onQueryHKFundRsp)
.def("onQueryHKMinPriceUnitRsp", &TdApi::onQueryHKMinPriceUnitRsp)
.def("onQueryHKTradeCalendarRsp", &TdApi::onQueryHKTradeCalendarRsp)
.def("onQueryLockSecurityDetailRsp", &TdApi::onQueryLockSecurityDetailRsp)
.def("onQueryTransferFundHistoryRsp", &TdApi::onQueryTransferFundHistoryRsp)
.def("onQueryCreditDebtsFlowRsp", &TdApi::onQueryCreditDebtsFlowRsp)
.def("onQueryCreditAssetFlowRsp", &TdApi::onQueryCreditAssetFlowRsp)
.def("onQueryCreditDebtsRsp", &TdApi::onQueryCreditDebtsRsp)
.def("onMicroServiceRsp", &TdApi::onMicroServiceRsp)
.def("onQueryBankBalanceRsp", &TdApi::onQueryBankBalanceRsp)
.def("onQueryBankInfoRsp", &TdApi::onQueryBankInfoRsp)
.def("onBankSecTransferRsp", &TdApi::onBankSecTransferRsp)
.def("onQueryBankSecTransferRsp", &TdApi::onQueryBankSecTransferRsp)
.def("onQueryHisBankSecTransferRsp", &TdApi::onQueryHisBankSecTransferRsp)
.def("onFundAccountTransferRsp", &TdApi::onFundAccountTransferRsp)
.def("onQueryFundAccountTransferRsp", &TdApi::onQueryFundAccountTransferRsp)
.def("onQueryHisOrderRsp", &TdApi::onQueryHisOrderRsp)
.def("onQueryHisTradeRsp", &TdApi::onQueryHisTradeRsp)
.def("onQueryDeliveryOrderRsp", &TdApi::onQueryDeliveryOrderRsp)
.def("onQueryStateOrderRsp", &TdApi::onQueryStateOrderRsp)
.def("onQueryExchangeListsRsp", &TdApi::onQueryExchangeListsRsp)
.def("onModifyPasswordRsp", &TdApi::onModifyPasswordRsp)
.def("onQueryPHXXRsp", &TdApi::onQueryPHXXRsp)
.def("onQueryZQXXRsp", &TdApi::onQueryZQXXRsp)
.def("onQueryLockSecurityContractRsp", &TdApi::onQueryLockSecurityContractRsp)
.def("onQueryCreditContractRsp", &TdApi::onQueryCreditContractRsp)
.def("onQueryCreditDebtsCollectRsp", &TdApi::onQueryCreditDebtsCollectRsp)
.def("onQueryCreditDataRsp", &TdApi::onQueryCreditDataRsp)
.def("onQueryPreMaturityDebtsRsp", &TdApi::onQueryPreMaturityDebtsRsp)
.def("onExtendPreMaturityDebtsRsp", &TdApi::onExtendPreMaturityDebtsRsp)
.def("onQueryPreMaturityDebtsExtensionRsp", &TdApi::onQueryPreMaturityDebtsExtensionRsp)
.def("onQueryVoteProposalRsp", &TdApi::onQueryVoteProposalRsp)
.def("onQueryCreditVoteCountRsp", &TdApi::onQueryCreditVoteCountRsp)
.def("onQueryCreditVoteRsp", &TdApi::onQueryCreditVoteRsp)
.def("onQueryNetVoteRightsRsp", &TdApi::onQueryNetVoteRightsRsp)
.def("onQueryNetVoteResultRsp", &TdApi::onQueryNetVoteResultRsp)
.def("onQueryNetVoteCountRsp", &TdApi::onQueryNetVoteCountRsp)
.def("onQueryStkConcentrationRsp", &TdApi::onQueryStkConcentrationRsp)
.def("onQueryHKHisOrderRsp", &TdApi::onQueryHKHisOrderRsp)
.def("onQueryWithdrawCashRsp", &TdApi::onQueryWithdrawCashRsp)
.def("onQueryNetVoteOrderRsp", &TdApi::onQueryNetVoteOrderRsp)
.def("onQueryTradeTotalRsp", &TdApi::onQueryTradeTotalRsp)
.def("onETFSubscriptCancelRsp", &TdApi::onETFSubscriptCancelRsp)
.def("onNetVoteOrderRsp", &TdApi::onNetVoteOrderRsp)
.def("onCreditNetVoteOrderRsp", &TdApi::onCreditNetVoteOrderRsp)
.def("onQueryMSCashRsp", &TdApi::onQueryMSCashRsp)
.def("onQueryMSPositionsRsp", &TdApi::onQueryMSPositionsRsp)
.def("onQueryMSCreditDebtsFlowRsp", &TdApi::onQueryMSCreditDebtsFlowRsp)
;
