## _*_ coding:UTF-8 _*_
import pandas as pd
import numpy as np

date = raw_input("Please input the Date (Format: eg. 2017-08-30):")
cusid = raw_input("Please input the customer ID with the company standard:")
#sc=float(raw_input("Please input the collateral rate for SC (Format: eg. 0.07):"))

ssbzj=pd.read_csv("ssbzj.csv",encoding='gbk')
khxx=pd.read_csv("khxx.csv",encoding='gbk')
bzjmb=pd.read_csv("bzjmb.csv",encoding='gbk')
customer=pd.read_csv(cusid+".csv",encoding='gbk')

exchange=pd.read_csv(ur"ref\指定交易日交易所保证金率查询_"+date+".csv",encoding='utf-8')
exchange[u'合约']=map(lambda x: x.upper(),exchange[u"合约"])
delta=pd.read_csv(ur"ref\投资者保证金率属性_"+date+".csv",encoding='utf-8')
delta[u'合约代码']=map(lambda x: x.upper(),delta[u"合约代码"])
standard=pd.read_csv(ur"ref\投资者保证金率_"+date+".csv",encoding='utf-8')
standard[u'合约']=map(lambda x: x.upper(),standard[u"合约"])
exchangesx=pd.read_csv(ur"ref\交易所保证金率属性_"+date+".csv",encoding='utf-8')
exchangesx[u'合约代码']=map(lambda x: x.upper(),exchangesx[u"合约代码"])

#核对交易所合约保证金
contract=[]
for index in ssbzj.index:
    if ssbzj.loc[index][u'合约代码'] == ssbzj.loc[index][u'合约代码']:
        contract.append(str(ssbzj.loc[index][u'品种编号'])+str(int(ssbzj.loc[index][u'合约代码'])))
    else:
        contract.append(ssbzj.loc[index][u'品种编号'])
contract1=pd.Series(contract)
ssbzj['contract'] = contract1.values

temp1=pd.merge(ssbzj,exchange,left_on='contract',right_on=u'合约')
for index in temp1.index:
    a1 = temp1.loc[index][u'初始保证金']
    a2 = temp1.loc[index][u'投机多头保证金率']
    if a1 != a2:
        if temp1.loc[index][u'投机套保'] != u'保值':
            print u"请核对合约上手保证金 " + temp1.loc[index]['contract']

#核对交易所品种保证金
#exchange[u"合约"].replace(regex=True, inplace=True, to_replace=r'[0-9.*]', value=r'')
#exchange=exchange.loc[exchange.groupby(exchange[u'合约'])[u'投机多头保证金率'].idxmin()]
exchangesx1=exchangesx[exchangesx[u'保证金分段名称'].isin([u'上市月后含1个交易日',u'上市月后含3个周五后含1个交易日后1个交易日'])]
#exchange[u"品种保证金"] = (exchange.groupby([u'合约'])[u'投机多头保证金率'].transform(lambda x: x.value_counts().index[0]))
protemp1=pd.merge(ssbzj,exchangesx1,left_on='contract',right_on=u'合约代码')
#protemp1.to_csv("test1.csv",encoding="utf8")
for index in protemp1.index:
    a1 = protemp1.loc[index][u'初始保证金']
    a2 = protemp1.loc[index][u'投机多头保证金率']
    a3 = protemp1.loc[index][u'保值多头保证金率']
    if a1 != a2:
        if protemp1.loc[index][u'投机套保'] != u'保值':
            print u"请核对品种上手保证金 " + protemp1.loc[index]['contract']
        else:
            if a1 != a3:
                print u"请核对品种上手保证金 " + protemp1.loc[index]['contract']
    """
    a1float = np.asscalar(a1)
    if a1 != a2:
        if protemp1.loc[index][u'投机套保'] != u'保值':
            if protemp1.loc[index][u'合约'] != "SC":
                print u"请核对品种上手保证金 " + protemp1.loc[index][u'合约']
            elif abs(a1float-sc) > 1e-9:
                print u"请核对品种上手保证金 SC"
    """

#核对保证金模板
bzjmb['contractproduct']=bzjmb[u'模板编号']+bzjmb[u'品种编号']
tempmb=pd.merge(bzjmb,khxx,left_on=u'模板编号',right_on=u'客户账号')
delta['contractproduct']=delta[u'投资者代码'].map(str)+delta[u'合约代码']
tempmb1=pd.merge(tempmb,delta,on='contractproduct')
#tempmb1.to_csv("test1.csv",encoding="utf8")
for index in tempmb1.index:
    a1 = tempmb1.loc[index][u'初始保证金']
    a2 = tempmb1.loc[index][u'投机多头保证金率']
    if tempmb1.loc[index][u'账号状态'] == u'正常':
        if a1 != a2:
            print u"请核对保证金模板 " + tempmb1.loc[index][u'模板编号'] + " " + tempmb1.loc[index][u'品种编号']

#核对公司标准客户最终费率
contractzz=[]
for index in customer.index:
    if customer.loc[index][u'合约'] == customer.loc[index][u'合约']:
        contractzz.append(str(customer.loc[index][u'品种编号'])+str(int(customer.loc[index][u'合约'])))
    else:
        contractzz.append(customer.loc[index][u'品种编号'])
contractzz1=pd.Series(contractzz)
customer['contractzz'] = contractzz1.values

temp1=pd.merge(customer,standard,left_on='contractzz',right_on=u'合约')
for index in temp1.index:
    a1 = temp1.loc[index][u'买投机初始保证金']
    a2 = temp1.loc[index][u'投机多头保证金率']
    if temp1.loc[index][u'品种类型'] == u"期货":
        if a1 != a2:
            print u"请核对最终费率 " + cusid + " " + temp1.loc[index]['contractzz']

raw_input("ALL COMPLETED")
