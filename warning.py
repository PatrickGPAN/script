## _*_ coding:UTF-8 _*_
import pandas as pd
import datetime
from qqbot import _bot as bot

def contract(exchange):
    data=pd.read_csv(exchange+today1+"InstrumentInfo.csv",encoding='gbk')
    contractL=[]
    for indexs in data.index:
        boardingdate=data.loc[indexs].values[11]
        if str(boardingdate) == nextdate1:
            contractL.append(data.loc[indexs].values[1])
    str1=''.join(contractL)
    print u'【'+exchange+u'新合约】 ' + str1 + ''
    bot.SendTo(bl[0], u'【'+exchange+u'新合约】 ' + str1 + '')

if __name__=='__main__':
    ONE_DAY=datetime.timedelta(days=1)
    today=datetime.date.today()
    nextdate=datetime.date.today()+ONE_DAY
    nextdate1=datetime.datetime.strftime(nextdate,'%Y%m%d')
    today1=datetime.datetime.strftime(today,'%Y%m%d')
    print "Next business day:" + nextdate1
    L=['SHFE','INE']
    bot.Login(['-q', ''])
    bl = bot.List('buddy', u'')
    for item in L:
        contract(item)
