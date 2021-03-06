#coding=utf-8
import csv
import time
import os
import pandas as pd
import re
import easygui

Dic={"人民币":"CNY","美元":"USD","货币质入":"Pledge","货币质出":"Redemption","大商所":"DCE","上期所":"SHFE","郑商所":"CZCE","能源中心":"INE","中金所":"CFFEX","买":"Buy","卖":"Sell","出入金":"Deposit/Withdrawal","银期转帐":"Bank-Futures Transfer","银期换汇":"Bank-Futures FX Exchange","开":"Open","平":"Close","平今":"Close Today","强平":"Forced Liquidation","平昨":"Close Prev.","强减":"Forced Reduction","本地强平":"Local Forced Liquidation","投":"Speculation","保":"Hedge","套":"Arbitrage","般":"General","市":"MarketMaker","线型低密度聚乙烯":"l","精对苯二甲酸":"TA","聚丙烯":"pp","天然橡胶":"ru","铝":"al","锌":"zn","铜":"cu","线材":"wr","螺纹钢":"rb","黄金":"au","白银":"ag","铅":"pb","燃料油":"fu","石油沥青":"bu","热轧卷板":"hc","镍":"ni","锡":"sn","黄玉米":"c","黄大豆1号":"a","黄大豆2号":"b","豆粕":"m","豆油":"y","棕榈油":"p","聚乙烯":"l","聚氯乙烯":"v","铁矿石":"i","焦煤":"jm","冶金焦炭":"j","鲜鸡蛋":"jd","中密度纤维板":"fb","细木工板":"bb","聚丙烯":"pp","玉米淀粉":"cs","一号棉花":"CF","PTA":"TA","菜籽油":"OI","优质强筋小麦":"WH","早籼稻":"RI","晚籼稻":"LR","白砂糖":"SR","玻璃":"FG","甲醇":"MA","普通小麦":"PM","菜籽粕":"RM","油菜籽":"RS","动力煤":"ZC","粳稻谷":"JR","硅铁":"SF","锰硅":"SM","棉纱":"CY","鲜苹果":"AP","沪深300指数":"IF","5年期国债":"TF","10年期国债":"T","上证50指数":"IH","中证500指数":"IC","原油":"sc","豆粕期权":"m_o"}
cusid=raw_input("Please input the customer ID:")
#date=raw_input("Please input the Date (Format: eg. 20170830):")
date=time.strftime("%Y%m%d")

print "###START TO GENERATE SETTLEMENT STATEMENT###"
os.makedirs(cusid+"_"+date)
print "Directory making"

# Account Summary CNY
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    blk_begin = '资金状况  币种：人民币 Account Summary  Currency:CNY'
    blk_end = '货币质押变化金额'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if blk_begin in line:
            write_block = True
        if write_block:
            data.append(line)
        if blk_end in line:
            write_block=False
    del data[0],data[0]
    L=[]
    K=[]
    M=[]
    header=['Balance b/f','Deposit/Withdrawal','Realized P/L','MTM P/L','Exercise P/L','Commission','Exercise Fee','Delivery Fee','New FX Pledge','FX Redemption','Chg in Pledge Amt','premium received','premium paid','Chg in FX Pledge','Initial Margin','Balance c/f','Pledge Amount','Client Equity','FX Pledge Occ','Margin Occupied','Delivery Margin','market value(long)','market value(short)','market value(equity)','Fund Avail.','Risk Degree','Margin Call']
    M.append(header)
    for item in data:
        L1=item.split("       ")
        L2=[x for x in L1 if x]
        L.append(L2[1])
    for item in data:
        L1=item.split("       ")
        L2=[x for x in L1 if x]
        if len(L2)>3:
            L.append(L2[3])
    for item in L:
        j=item.replace(' ','')
        K.append(j)
    M.append(K)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_AccountSummary_CNY.csv", "wb") as fp:
        for item in M:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Account Summary CNY Completed"

# Account Summary USD
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    blk_begin = '资金状况  币种：美元 Account Summary  Currency:USD'
    blk_end = '货币质押变化金额'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if line == blk_begin:
            write_block = True
        if write_block:
            data.append(line)
        if blk_end in line:
            write_block=False
    del data[0],data[0]
    L=[]
    K=[]
    M=[]
    header=['Balance b/f','Deposit/Withdrawal','Realized P/L','MTM P/L','Exercise P/L','Commission','Exercise Fee','Delivery Fee','New FX Pledge','FX Redemption','Chg in Pledge Amt','premium received','premium paid', 'Chg in FX Pledge','Initial Margin','Balance c/f','Pledge Amount','Client Equity','FX Pledge Occ','Margin Occupied','Delivery Margin','market value(long)','market value(short)','market value(equity)','Fund Avail.','Risk Degree','Margin Call']
    M.append(header)
    for item in data:
        L1=item.split("       ")
        L2=[x for x in L1 if x]
        L.append(L2[1])
    for item in data:
        L1=item.split("       ")
        L2=[x for x in L1 if x]
        if len(L2)>3:
            L.append(L2[3])
    for item in L:
        j=item.replace(' ','')
        K.append(j)
    M.append(K)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_AccountSummary_USD.csv", "wb") as fp:
        for item in M:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Account Summary USD Completed"

#Deposit/Withdrawal CNY
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    mark = '资金状况  币种：美元 Account Summary  Currency:USD'
    blk_begin = '出入金明细 Deposit/Withdrawal'
    blk_end = '----------------------------------------------------------------------------------------------------------------------'
    i=0
    for line in f:
        line=line.strip()
        i=i+1
        if line==mark:
            j=i
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        i=i+1
        if line == blk_begin:
            if i<j:
                write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==4:
            write_block=False
    if data:
        del data[-3]
    data1=data[5:-1]
    TR = []
    header = ['Date','Type','Deposit','Withdrawal','Note']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_DepositWithdrawal_CNY.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Deposit/Withdrawal CNY Completed"

#Deposit/Withdrawal USD
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    mark = '资金状况  币种：美元 Account Summary  Currency:USD'
    blk_begin = '出入金明细 Deposit/Withdrawal'
    blk_end = '----------------------------------------------------------------------------------------------------------------------'
    write_block = False
    tag=1
    data=[]
    for line in f:
        line=line.strip()
        if mark in line:
            tag=0
        if tag==0:
            if blk_begin in line:
                write_block = True
            if write_block:
                data.append(line)
            if data.count(blk_end)==4:
                write_block=False
    data1=data[5:-1]
    TR = []
    header = ['Date','Type','Deposit','Withdrawal','Note']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_DepositWithdrawal_USD.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Deposit/Withdrawal USD Completed"

#货币质押 FX Pledge CNY
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    mark = '资金状况  币种：美元 Account Summary  Currency:USD'
    blk_begin = '货币质押 FX Pledge'
    blk_end = '-------------------------------------------------------------------------------------------------------------'
    data=[]
    write_block = False
    tag=0
    for line in f:
        line=line.strip()
        if tag==0:
            if line == blk_begin:
                write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==3:
            write_block=False
        if mark in line:
            tag=1
    data1=data[5:-1]
    lenfpcny=str(len(data1))
    TR = []
    header = ['Date','Exchange','Amount','Direction','Rate','Discount','Currency','Amount']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_FXPledge_CNY.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "FX Pledge CNY Completed"

#货币质押 FX Pledge USD
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    mark = '资金状况  币种：美元 Account Summary  Currency:USD'
    blk_begin = '货币质押 FX Pledge'
    blk_end = '-------------------------------------------------------------------------------------------------------------'
    data=[]
    write_block = False
    tag=0
    for line in f:
        line=line.strip()
        if mark in line:
            tag=1
        if tag==1:
            if line == blk_begin:
                write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==3:
            write_block=False
    data1=data[5:-1]
    lenfpusd=str(len(data1))
    TR = []
    header = ['Date','Exchange','Amount','Direction','Rate','Discount','Currency','Amount']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_FXPledge_USD.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "FX Pledge USD Completed"

#Warrant Pledge
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt","r") as f:
    blk_begin = '质押明细 Warrant Pledge'
    blk_end = '----------------------------------------------------------------------'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if line == blk_begin:
            write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==3:
            write_block=False
    data1=data[5:-1]
    lenwp=str(len(data1))
    TR = []
    header = ['Trans. Date','Code','Name','Qty','Amount']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_WarrantPledge.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "WarrantPledge Completed"

#Transaction Record
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt", "r") as f:
    blk_begin = '成交记录 Transaction Record'
    blk_end = '---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if line == blk_begin:
            write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==4:
            write_block=False
    if data:
        del data[-3]
    data1=data[5:-1]
    TR = []
    header = ['Date', 'Exchange', 'Product', 'Instrument', 'B/S', 'S/H', 'Price', 'Lots', 'Turnover', 'O/C', 'Fee','Realized P/L', 'Premium Received/Paid', 'Trans.No.']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_TransactionRecord.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "TransactionRecord Completed"

#Position Closed
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt", "r") as f:
    blk_begin = '平仓明细 Position Closed'
    blk_end = '-------------------------------------------------------------------------------------------------------------------------------------------------------------'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if line == blk_begin:
            write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==4:
            write_block=False
    if data:
        del data[-3]
    data1=data[5:-1]
    TR = []
    header = ['Close Date','Exchange','Product','Instrument','Open Date','B/S','Lots','Pos. Open Price','Prev. Sttl','Trans. Price','Realized P/L','Premium Received/Paid']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_PositionClosed.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Position Closed Completed"

#Positions Detail
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt", "r") as f:
    blk_begin = '持仓明细 Positions Detail'
    blk_end = '-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if line == blk_begin:
            write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==4:
            write_block=False
    if data:
        del data[-3]
    data1=data[5:-1]
    TR = []
    header = ['Exchange','Product','Instrument','Open Date','S/H','B/S','Positon','Pos. Open Price','Prev. Sttl','Settlement Price','Accum. P/L','MTM P/L','Margin','Market Value(Options)']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_PositionsDetail.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Positions Detail Completed"

#Positions
with open(date+"_"+cusid+u"_交易结算单（Settlement Statement）.txt", "r") as f:
    blk_begin = '持仓汇总 Positions'
    blk_end = '---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    data=[]
    write_block = False
    for line in f:
        line=line.strip()
        if line == blk_begin:
            write_block = True
        if write_block:
            data.append(line)
        if data.count(blk_end)==4:
            write_block=False
    if data:
        del data[-3]
    data1=data[5:-1]
    TR = []
    header = ['Product','Instrument','Long Pos.','Avg Buy Price','Short Pos.','Avg Sell Price','Prev. Sttl','Sttl Today','MTM P/L','Margin Occupied','S/H','Market Value(Long)','Market Value(Short)']
    TR.append(header)
    for item in data1:
        DL=item.split("|")
        LTR=[]
        for item in DL:
            M=item.replace(' ','')
            LTR.append(M)
        LTR2 = [x for x in LTR if x]
        LTR3=[]
        for item in LTR2:
            if item in Dic.keys():
                item=Dic[item]
                LTR3.append(item)
            else:
                LTR3.append(item)
        TR.append(LTR3)
    with open(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_Positions.csv", "wb") as fp:
        for item in TR:
            wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
            wr.writerow(item)
print "Positions Completed"
print "###START TO VERIFY THE SETTLEMENT STATEMENT###"

#Verification
#Account summary
pdac=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_AccountSummary_CNY.csv")
equ=pdac.iloc[0]['Balance b/f']+pdac.iloc[0]['Deposit/Withdrawal']-pdac.iloc[0]['Commission']-pdac.iloc[0]['Exercise Fee']-pdac.iloc[0]['Delivery Fee']+pdac.iloc[0]['Realized P/L']+pdac.iloc[0]['MTM P/L']+pdac.iloc[0]['Exercise P/L']+pdac.iloc[0]['Chg in Pledge Amt']+pdac.iloc[0]['premium received']-pdac.iloc[0]['premium paid']+pdac.iloc[0]['Chg in FX Pledge']
if str(pdac.iloc[0]['Client Equity'])!=str(equ):
    easygui.msgbox("请查看AccountSummary_CNY的期末权益", title="Reminder", ok_button="OK")
else:
    print "Client Equity with CNY has been verified"

if pdac.iloc[0]['FX Pledge Occ']<pdac.iloc[0]['Margin Occupied']:
    if str(pdac.iloc[0]['Fund Avail.'])!=str(pdac.iloc[0]['Client Equity']-pdac.iloc[0]['Margin Occupied']-pdac.iloc[0]['New FX Pledge']):
        easygui.msgbox("请查看AccountSummary_CNY的可用资金", title="Reminder", ok_button="OK")
    else:
        print "Fund avaliable with CNY has been verified"
elif pdac.iloc[0]['FX Pledge Occ']>=pdac.iloc[0]['Margin Occupied']:
    if str(pdac.iloc[0]['Fund Avail.'])!=str(pdac.iloc[0]['Client Equity']-pdac.iloc[0]['New FX Pledge']):
        easygui.msgbox("请查看AccountSummary_CNY的可用资金", title="Reminder", ok_button="OK")
    else:
        print "Fund avaliable with CNY has been verified"

pdac=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_AccountSummary_USD.csv")
"""
equ=pdac.iloc[0]['Balance b/f']+pdac.iloc[0]['Deposit/Withdrawal']-pdac.iloc[0]['Commission']-pdac.iloc[0]['Exercise Fee']-pdac.iloc[0]['Delivery Fee']+pdac.iloc[0]['Realized P/L']+pdac.iloc[0]['MTM P/L']+pdac.iloc[0]['Exercise P/L']+pdac.iloc[0]['Chg in Pledge Amt']+pdac.iloc[0]['premium received']-pdac.iloc[0]['premium paid']+pdac.iloc[0]['Chg in FX Pledge']
if str(pdac.iloc[0]['Client Equity'])!=str(equ):
    easygui.msgbox("请查看AccountSummary_USD的期末权益", title="Reminder", ok_button="OK")
else:
    print "Client Equity with USD has been verified"
"""
if pdac.iloc[0]['FX Pledge Occ']<pdac.iloc[0]['Margin Occupied']:
    if str(pdac.iloc[0]['Fund Avail.'])!=str(pdac.iloc[0]['Client Equity']-pdac.iloc[0]['Margin Occupied']-pdac.iloc[0]['New FX Pledge']):
        easygui.msgbox("请查看AccountSummary_USD的可用资金", title="Reminder", ok_button="OK")
    else:
        print "Fund avaliable with USD has been verified"
elif pdac.iloc[0]['FX Pledge Occ']>=pdac.iloc[0]['Margin Occupied']:
    if str(pdac.iloc[0]['Fund Avail.'])!=str(pdac.iloc[0]['Client Equity']-pdac.iloc[0]['New FX Pledge']):
        easygui.msgbox("请查看AccountSummary_USD的可用资金", title="Reminder", ok_button="OK")
    else:
        print "Fund avaliable with USD has been verified"

#Deposit/Withdrawal
pdDW=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_DepositWithdrawal_CNY.csv")
if len(pdDW)!= 0:
    pd1=pdDW[:-2]
    sum=pdDW.tail(1)

    #row
    num=str(len(pd1))
    num1=sum.iloc[0][0]
    num2=re.findall('\d+', num1)[0]
    if num==num2:
        print "Deposit/Withdrawal_CNY rows verified"
    else:
        easygui.msgbox("请查看Deposit/Withdrawal with CNY的行数", title="Reminder", ok_button="OK")
    #summary
    sum1="%0.2f" %(float(sum.iloc[0][1]),)
    sum2="%0.2f" %(float(sum.iloc[0][2]),)
    #sum Deposit
    depositsum="%0.2f" %(pd1['Deposit'].sum(),)
    if sum1==depositsum:
        print "Deposit/Withdrawal_CNY Deposit Cloumn verified"
    else:
        easygui.msgbox("请查看Deposit/Withdrawal with CNY的deposit列", title="Reminder", ok_button="OK")
    #sum Withdrawl
    withdrawlsum="%0.2f" %(pd1["Withdrawal"].sum(),)
    if sum2==withdrawlsum:
        print "Deposit/Withdrawal with CNY Withdrawl Cloumn verified"
    else:
        easygui.msgbox("请查看Deposit/Withdrawal with CNY的withdrawl列", title="Reminder", ok_button="OK")
    #delete the last row
    pd1.to_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_DepositWithdrawal_CNY.csv",index=False)

pdDW=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_DepositWithdrawal_USD.csv")
if len(pdDW)!= 0:
    pd1=pdDW[:-2]
    sum=pdDW.tail(1)

    #row
    num=str(len(pd1))
    num1=sum.iloc[0][0]
    num2=re.findall('\d+', num1)[0]
    if num==num2:
        print "Deposit/Withdrawal_USD rows verified"
    else:
        easygui.msgbox("请查看Deposit/Withdrawal with USD的行数", title="Reminder", ok_button="OK")
    #summary
    sum1="%0.2f" %(float(sum.iloc[0][1]),)
    sum2="%0.2f" %(float(sum.iloc[0][2]),)
    #sum Deposit
    depositsum="%0.2f" %(pd1['Deposit'].sum(),)
    if sum1==depositsum:
        print "Deposit/Withdrawal_USD Deposit Cloumn verified"
    else:
        easygui.msgbox("请查看Deposit/Withdrawal with USD的deposit列", title="Reminder", ok_button="OK")
    #sum Withdrawl
    withdrawlsum="%0.2f" %(pd1["Withdrawal"].sum(),)
    if sum2==withdrawlsum:
        print "Deposit/Withdrawal with USD Withdrawl Cloumn verified"
    else:
        easygui.msgbox("请查看Deposit/Withdrawal with USD的withdrawl列", title="Reminder", ok_button="OK")
    #delete the last row
    pd1.to_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_DepositWithdrawal_USD.csv",index=False)

#货币质押 FX Pledge
pdwp=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_FXPledge_CNY.csv")
if len(pdwp)!=0:
    num=str(len(pdwp))
    if num==lenfpcny:
        print "FXPledge_CNY rows verified"
    else:
        easygui.msgbox("请查看FXPledge with CNY的行数", title="Reminder", ok_button="OK")
pdwp=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_FXPledge_USD.csv")
if len(pdwp)!=0:
    num=str(len(pdwp))
    if num==lenfpusd:
        print "FXPledge_USD rows verified"
    else:
        easygui.msgbox("请查看FXPledge with USD的行数", title="Reminder", ok_button="OK")

#Warrant Pledge
pdwp=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_WarrantPledge.csv")
if len(pdwp)!=0:
    num=str(len(pdwp))
    if num==lenwp:
        print "Warrant Pledge rows verified"
    else:
        easygui.msgbox("请查看Warrant Pledge的行数", title="Reminder", ok_button="OK")

#Transaction Record
pdtr=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_TransactionRecord.csv")
if len(pdtr)!=0:
    pd1=pdtr[:-1]
    sum=pdtr.tail(1)

    #row
    num=str(len(pd1))
    num1=sum.iloc[0][0]
    num2=re.findall('\d+', num1)[0]
    if num==num2:
        print "Transaction Record rows verified"
    else:
        easygui.msgbox("请查看Transaction Record的行数", title="Reminder", ok_button="OK")

    #summary
    sum1="%0.2f" %(float(sum.iloc[0][1]),)
    sum2="%0.2f" %(float(sum.iloc[0][2]),)
    sum3="%0.2f" %(float(sum.iloc[0][3]),)
    sum4="%0.2f" %(float(sum.iloc[0][4]),)
    sum5="%0.2f" %(float(sum.iloc[0][5]),)

    #sum Lots
    depositsum="%0.2f" %(pd1['Lots'].sum(),)
    if sum1==depositsum:
        print "Transaction Record Lots Cloumn verified"
    else:
        easygui.msgbox("请查看Transaction Record的Lots列", title="Reminder", ok_button="OK")

    #sum Turnover
    trunoversum="%0.2f" %(pd1['Turnover'].sum(),)
    if sum2==trunoversum:
        print "Transaction Record Turnover Cloumn verified"
    else:
        easygui.msgbox("请查看Transaction Record的Turnover列", title="Reminder", ok_button="OK")

    #Fee
    feesum="%0.2f" %(pd1['Fee'].sum(),)
    if sum3==feesum:
        print "Transaction Record Fee Cloumn verified"
    else:
        easygui.msgbox("请查看Transaction Record的Fee列", title="Reminder", ok_button="OK")

    #Realized P/L
    plsum="%0.2f" %(pd1['Realized P/L'].sum(),)
    if sum4==plsum:
        print "Transaction Record Realized P/L Cloumn verified"
    else:
        easygui.msgbox("请查看Transaction Record的Realized P/L列", title="Reminder", ok_button="OK")

    #Premium Received/Paid
    rpsum="%0.2f" %(pd1['Premium Received/Paid'].sum(),)
    if sum5==rpsum:
        print "Transaction Record Premium Received/Paid Cloumn verified"
    else:
        easygui.msgbox("请查看Transaction Record的Premium Received/Paid列", title="Reminder", ok_button="OK")
    #delete the last row
    pd1.to_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_TransactionRecord.csv",index=False)

#Position Closed
pdpc=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_PositionClosed.csv")
if len(pdpc)!=0:
    pd1=pdpc[:-1]
    sum=pdpc.tail(1)

    #row
    num=str(len(pd1))
    num1=sum.iloc[0][0]
    num2=re.findall('\d+', num1)[0]
    if num==num2:
        print "Position Closed rows verified"
    else:
        easygui.msgbox("请查看Position Closed的行数", title="Reminder", ok_button="OK")
    #summary
    sum1="%0.2f" %(float(sum.iloc[0][1]),)
    sum2="%0.2f" %(float(sum.iloc[0][2]),)
    sum3="%0.2f" %(float(sum.iloc[0][3]),)
    #sum Deposit
    depositsum="%0.2f" %(pd1['Lots'].sum(),)
    if sum1==depositsum:
        print "Position Closed Lots Cloumn verified"
    else:
        easygui.msgbox("请查看Position Closed的Lots列", title="Reminder", ok_button="OK")

    plsum="%0.2f" %(pd1['Realized P/L'].sum(),)
    if sum2==plsum:
        print "Position Closed Realized P/L Cloumn verified"
    else:
        easygui.msgbox("请查看Position Closed的Realized P/L列", title="Reminder", ok_button="OK")

    rpsum="%0.2f" %(pd1['Premium Received/Paid'].sum(),)
    if sum3==rpsum:
        print "Position Closed Premium Received/Paid Cloumn verified"
    else:
        easygui.msgbox("请查看Position Closed的Premium Received/Paid列", title="Reminder", ok_button="OK")
    #delete the last row
    pd1.to_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_PositionClosed.csv",index=False)

#Positions Detail
pdpc=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_PositionsDetail.csv")
if len(pdpc)!=0:
    pd1=pdpc[:-1]
    sum=pdpc.tail(1)

    #row
    num=str(len(pd1))
    num1=sum.iloc[0][0]
    num2=re.findall('\d+', num1)[0]
    if num==num2:
        print "Positions Detail rows verified"
    else:
        easygui.msgbox("请查看Positions Detail的行数", title="Reminder", ok_button="OK")
    #summary
    sum1="%0.2f" %(float(sum.iloc[0][1]),)
    sum2="%0.2f" %(float(sum.iloc[0][2]),)
    sum3="%0.2f" %(float(sum.iloc[0][3]),)
    sum4="%0.2f" %(float(sum.iloc[0][4]),)
    sum5="%0.2f" %(float(sum.iloc[0][5]),)
    #sum41="%0.2f" % (sum4,)
    #sum Deposit
    depositsum="%0.2f" %(pd1['Positon'].sum(),)
    if sum1==depositsum:
        print "Positions Detail Positon Cloumn verified"
    else:
        easygui.msgbox("请查看Positions Detail的Positon列", title="Reminder", ok_button="OK")

    plsum="%0.2f" %(pd1['Accum. P/L'].sum(),)
    if sum2==plsum:
        print "Positions Detail Accum. P/L Cloumn verified"
    else:
        easygui.msgbox("请查看Positions Detail的Accum. P/L列", title="Reminder", ok_button="OK")

    rpsum="%0.2f" %(pd1['MTM P/L'].sum(),)
    if sum3==rpsum:
        print "Positions Detail MTM P/L Cloumn verified"
    else:
        easygui.msgbox("请查看Positions Detail的MTM P/L列", title="Reminder", ok_button="OK")

    rpsum="%0.2f" %(pd1['Margin'].sum(),)
    if sum4==rpsum:
        print "Positions Detail Margin Cloumn verified"
    else:
        easygui.msgbox("请查看Positions Detail的Margin列", title="Reminder", ok_button="OK")

    rpsum="%0.2f" %(pd1['Market Value(Options)'].sum(),)
    if sum5==rpsum:
        print "Positions Detail Market Value(Options) Cloumn verified"
    else:
        easygui.msgbox("请查看Positions Detail的Market Value(Options)列", title="Reminder", ok_button="OK")

    #delete the last row
    pd1.to_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_PositionsDetail.csv",index=False)

#Positions
pdpc=pd.read_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_Positions.csv")
if len(pdpc)!=0:
    pd1=pdpc[:-1]
    sum=pdpc.tail(1)

    #row
    num=str(len(pd1))
    num1=sum.iloc[0][0]
    num2=re.findall('\d+', num1)[0]
    if num==num2:
        print "Positions rows verified"
    else:
        easygui.msgbox("请查看Positions的行数", title="Reminder", ok_button="OK")
    #summary
    sum1="%0.2f" %(float(sum.iloc[0][1]),)
    sum2="%0.2f" %(float(sum.iloc[0][2]),)
    sum3="%0.2f" %(float(sum.iloc[0][3]),)
    sum4="%0.2f" %(float(sum.iloc[0][4]),)
    sum5="%0.2f" %(float(sum.iloc[0][5]),)
    sum6="%0.2f" %(float(sum.iloc[0][6]),)

    plsum="%0.2f" %(pd1['Long Pos.'].sum(),)
    if sum1==plsum:
        print "Positions Long Pos. Cloumn verified"
    else:
        easygui.msgbox("请查看Positions的Long Pos.列", title="Reminder", ok_button="OK")

    rpsum="%0.2f" %(pd1['Short Pos.'].sum(),)
    if sum2==rpsum:
        print "Positions Short Pos. Cloumn verified"
    else:
        easygui.msgbox("请查看Positions的Short Pos.列", title="Reminder", ok_button="OK")

    depositsum="%0.2f" %(pd1['MTM P/L'].sum(),)
    if sum3==depositsum:
        print "Positions MTM P/L Cloumn verified"
    else:
        easygui.msgbox("请查看Positions的MTM P/L列", title="Reminder", ok_button="OK")

    depositsum="%0.2f" %(pd1['Margin Occupied'].sum(),)
    if sum4==depositsum:
        print "Positions Margin Occupied Cloumn verified"
    else:
        easygui.msgbox("请查看Positions的Margin Occupied列", title="Reminder", ok_button="OK")

    depositsum="%0.2f" %(pd1['Market Value(Long)'].sum(),)
    if sum5==depositsum:
        print "Positions Market Value(Long) Cloumn verified"
    else:
        easygui.msgbox("请查看Positions的Market Value(Long)列", title="Reminder", ok_button="OK")

    depositsum="%0.2f" %(pd1['Market Value(Short)'].sum(),)
    if sum6==depositsum:
        print "Positions Market Value(Short) Cloumn verified"
    else:
        easygui.msgbox("请查看Positions的Market Value(Short)列", title="Reminder", ok_button="OK")

    #delete the last row
    pd1.to_csv(cusid+"_"+date+"/"+"0011_SG01_"+date+"_1_Positions.csv",index=False)

raw_input("###ALL COMPLETED###")
