# -*- coding: utf-8 -*-
"""
本模块功能：SIAT公共基础函数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2019年7月16日
最新修订日期：2020年3月28日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')

#==============================================================================
SUFFIX_LIST_CN=['SS','SZ','BJ','NQ']
import pandas as pd
#==============================================================================
#设置全局语言环境
import pickle

def check_language():
    """
    查询全局语言设置
    """
    try:
        with open('siat_language.pkl','rb') as file:
            lang=pickle.load(file)
    except:
        lang='Chinese'
        
    return lang

def set_language(lang='Chinese'):
    """
    修改全局语言设置
    """
    
    if lang in ['English','Chinese']:
        with open('siat_language.pkl','wb') as file:
            pickle.dump(lang,file)
        print("  Global language is set to",lang)
    else:
        print("  Warning: undefined language",lang)
        
    return

def text_lang(txtcn,txten):
    """
    功能：适应双语文字，中文环境返回txtcn，英文环境返回txten
    """
    lang=check_language()
    
    if lang=='Chinese': txt=txtcn
    else: txt=txten
    
    return txt
#==============================================================================
"""
def today():
    \"""
    返回今日的日期
    \"""
    import datetime; now=datetime.datetime.now()
    jinri=now.strftime("%Y-%m-%d")
    
    return jinri

if __name__=='__main__':
    today()
"""
#==============================================================================

def now():
    """
    返回今日的日期
    """
    import datetime; dttime=datetime.datetime.now()
    xianzai=dttime.strftime("%Y-%m-%d %H:%M:%S")
    
    return xianzai

if __name__=='__main__':
    now()
#==============================================================================

def hello():
    """
    返回当前环境信息
    """
    #当前系统信息
    import platform
    ossys=platform.system()
    (arch,_)=platform.architecture()
    osver=platform.platform()    
    print(ossys,arch,osver)
    
    #Python版本信息
    import sys
    pyver=sys.version
    pos=pyver.find(' ')
    pyver1=pyver[:pos]
    print("Python",pyver1,end=', ')
    
    #siat版本信息
    import pkg_resources
    siatver=pkg_resources.get_distribution("siat").version    
    print("siat",siatver)
    
    #运行环境
    import sys; pypath=sys.executable
    pos=pypath.rfind('\\')
                     
    pypath1=pypath[:pos]
    print("Located in",pypath1)

    from IPython import get_ipython
    ipy_str = str(type(get_ipython())) 
    if 'zmqshell' in ipy_str:
        print("Working in Jupyter environment")
    else:
        print("NOT in Jupyter environment")
    
    #当前日期时间
    print("Currently",now())
    
    return

if __name__=='__main__':
    hello()
#==============================================================================
def ticker_check(ticker, source="yahoo"):
    """
    检查证券代码，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码ticker，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #测试用，完了需要注释掉
    #ticker="600519.sh"
    #source="yahoo"
    
    #将字母转为大写
    ticker1=ticker.upper()
    #截取字符串最后2/3位
    suffix2=ticker1[-2:]
    suffix3=ticker1[-3:]
    
    #判断是否大陆证券
    if suffix3 in ['.SH', '.SS', '.SZ']:
        prc=True
    else: prc=False

    #根据数据源的格式修正大陆证券代码
    if (source == "yahoo") and (suffix3 in ['.SH']):
        ticker1=ticker1.replace(suffix3, '.SS')        
    if (source == "tushare") and (suffix3 in ['.SS']):
        ticker1=ticker1.replace(suffix3, '.SH')  

    #若为港交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共7位
    if suffix3 in ['.HK']:
        ticker1=ticker1[-7:]     

    #若为东交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共6位
    if suffix2 in ['.T']:
        ticker1=ticker1[-6:]  
    
    #返回：是否大陆证券，基于数据源/交易所格式修正后的证券代码
    return prc, ticker1        

#测试各种情形
if __name__=='__main__':
    prc, ticker=ticker_check("600519.sh","yahoo")
    print(prc,ticker)
    print(ticker_check("600519.SH","yahoo"))    
    print(ticker_check("600519.ss","yahoo"))    
    print(ticker_check("600519.SH","tushare"))    
    print(ticker_check("600519.ss","tushare"))    
    print(ticker_check("000002.sz","tushare"))
    print(ticker_check("000002.sz","yahoo"))
    print(ticker_check("00700.Hk","yahoo"))
    print(ticker_check("99830.t","yahoo"))

#==============================================================================
def tickers_check(tickers, source="yahoo"):
    """
    检查证券代码列表，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码列表tickers，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：证券代码列表，字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #检查列表是否为空
    if tickers[0] is None:
        print("*** 错误#1(tickers_check)，空的证券代码列表:",tickers)
        return None         
    
    tickers_new=[]
    for t in tickers:
        _, t_new = ticker_check(t, source=source)
        tickers_new.append(t_new)
    
    #返回：基于数据源/交易所格式修正后的证券代码
    return tickers_new

#测试各种情形
if __name__=='__main__':
    tickers=tickers_check(["600519.sh","000002.sz"],"yahoo")
    print(tickers)
#==============================================================================
def check_period(fromdate, todate):
    """
    功能：根据开始/结束日期检查日期与期间的合理性
    输入参数：
    fromdate：开始日期。格式：YYYY-MM-DD
    enddate：开始日期。格式：YYYY-MM-DD
    输出参数：
    validity：期间合理性。True-合理，False-不合理
    start：开始日期。格式：datetime类型
    end：结束日期。格式：datetime类型
    """
    import pandas as pd
    
    #测试开始日期的合理性
    try:
        start=pd.to_datetime(fromdate)
    except:
        print("*** #Error(check_period), invalid date:",fromdate)
        return None, None, None         
    
    #测试结束日期的合理性
    try:
        end=pd.to_datetime(todate)
    except:
        print("  #Error(check_period): invalid date:",todate)
        return None, None, None          
    
    #测试日期期间的合理性
    if start > end:
        print("  #Error(check_period): invalid period: from",fromdate,"to",todate)
        return None, None, None     

    return True, start, end

if __name__ =="__main__":
    check_period('2020-1-1','2020-2-4')
    check_period('2020-1-1','2010-2-4')
    
    start='2020-1-1'; end='2022-12-20'
    result,startpd,endpd=check_period(start,end)

#==============================================================================
def date_adjust(basedate, adjust=0):
    """
    功能：将给定日期向前或向后调整特定的天数
    输入：基础日期，需要调整的天数。
    basedate: 基础日期。
    adjust：需要调整的天数，负数表示向前调整，正数表示向后调整。
    输出：调整后的日期。
    """
    #检查基础日期的合理性
    import pandas as pd    
    try:
        bd=pd.to_datetime(basedate)
    except:
        print("  #Error(date_adjust): invalid:",basedate)
        return None

    #调整日期
    from datetime import timedelta
    nd = bd+timedelta(days=adjust)    
    
    #重新提取日期
    newdate=nd.date()   
    return str(newdate)
 
if __name__ =="__main__":
    basedate='2020-3-17' 
    adjust=-365    
    newdate = date_adjust(basedate, adjust)
    print(newdate)    

#==============================================================================
if __name__ =="__main__":
    portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}

def decompose_portfolio(portfolio):
    """
    功能：将一个投资组合字典分解为股票代码列表和份额列表
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合
    输出：市场，市场指数，股票代码列表和份额列表
    """
    #从字典中提取信息
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]

    return scope,mktidx,stocklist,portionlist    

if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    scope,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio1)
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio1)

def portfolio_name(portfolio):
    """
    功能：解析一个投资组合的名字
    输入：投资组合
    输出：投资组合的自定义名称，未定义的返回"投资组合"
    注意：为了维持兼容性，特此定义此函数
    """
    #从字典中提取信息
    keylist=list(portfolio.keys())
    try:
        name=portfolio[keylist[0]][2]
    except:
        name="投资组合"

    return name    

if __name__=='__main__':
    portfolio={'Market':('US','^GSPC','我的组合001'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    portfolio_name(portfolio)
    
#==============================================================================
def calc_monthly_date_range(start,end):
    """
    功能：返回两个日期之间各个月份的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个月份的开始和结束日期元组对列表
    """
    #测试用
    #start='2019-01-05'
    #end='2019-06-25'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当月的结束日期
    syear=startdate.year
    smonth=startdate.month
    import calendar
    sdays=calendar.monthrange(syear,smonth)[1]
    from datetime import date
    slastday=pd.to_datetime(date(syear,smonth,sdays))

    if slastday > enddate: slastday=enddate
    
    #加入第一月的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束月的开始和结束日期
    eyear=enddate.year
    emonth=enddate.month
    efirstday=pd.to_datetime(date(eyear,emonth,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个月份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(months=+1)
    while next < efirstday:
        nyear=next.year
        nmonth=next.month
        nextstart=pd.to_datetime(date(nyear,nmonth,1))
        ndays=calendar.monthrange(nyear,nmonth)[1]
        nextend=pd.to_datetime(date(nyear,nmonth,ndays))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(months=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_monthly_date_range('2019-01-01','2019-06-30')
    mdp2=calc_monthly_date_range('2000-01-01','2000-06-30')   #闰年
    mdp3=calc_monthly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)


#==============================================================================
def calc_yearly_date_range(start,end):
    """
    功能：返回两个日期之间各个年度的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个年度的开始和结束日期元组对列表
    """
    #测试用
    #start='2013-01-01'
    #end='2019-08-08'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当年的结束日期
    syear=startdate.year
    from datetime import date
    slastday=pd.to_datetime(date(syear,12,31))

    if slastday > enddate: slastday=enddate
    
    #加入第一年的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束年的开始和结束日期
    eyear=enddate.year
    efirstday=pd.to_datetime(date(eyear,1,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个年份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(years=+1)
    while next < efirstday:
        nyear=next.year
        nextstart=pd.to_datetime(date(nyear,1,1))
        nextend=pd.to_datetime(date(nyear,12,31))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(years=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_yearly_date_range('2013-01-05','2019-06-30')
    mdp2=calc_yearly_date_range('2000-01-01','2019-06-30')   #闰年
    mdp3=calc_yearly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)

#==============================================================================

def sample_selection(df,start,end):
    """
    功能：根据日期范围start/end选择数据集df的子样本，并返回子样本
    """
    flag,start2,end2=check_period(start,end)
    df_sub=df[df.index >= start2]
    df_sub=df_sub[df_sub.index <= end2]
    
    return df_sub
    
if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    market,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio)
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(tickerlist,sharelist,start,end)
    start2='2020-1-10'; end2='2020-3-18'
    df_sub=sample_selection(pfdf,start2,end2)    
    
#==============================================================================
def init_ts():
    """
    功能：初始化tushare pro，登录后才能下载数据
    """
    import tushare as ts
    #设置token
    token='49f134b05e668d288be43264639ac77821ab9938ff40d6013c0ed24f'
    pro=ts.pro_api(token)
    
    return pro
#==============================================================================
def convert_date_ts(y4m2d2):
    """
    功能：日期格式转换，YYYY-MM-DD-->YYYYMMDD，用于tushare
    输入：日期，格式：YYYY-MM-DD
    输出：日期，格式：YYYYMMDD
    """
    import pandas as pd
    try: date1=pd.to_datetime(y4m2d2)
    except:
        print("  #Error(convert_date_ts): invalid date:",y4m2d2)
        return None 
    else:
        date2=date1.strftime('%Y')+date1.strftime('%m')+date1.strftime('%d')
    return date2

if __name__ == '__main__':
    convert_date_ts("2019/11/1")
#==============================================================================
def gen_yearlist(start_year,end_year):
    """
    功能：产生从start_year到end_year的一个年度列表
    输入参数：
    start_year: 开始年份，字符串
    end_year：截止年份
    输出参数：
    年份字符串列表    
    """
    #仅为测试使用，完成后应注释掉
    #start_year='2010'
    #end_year='2019'    
    
    import numpy as np
    start=int(start_year)
    end=int(end_year)
    num=end-start+1    
    ylist=np.linspace(start,end,num=num,endpoint=True)
    
    yearlist=[]
    for y in ylist:
        yy='%d' %y
        yearlist=yearlist+[yy]
    #print(yearlist)
    
    return yearlist

if __name__=='__main__':
    yearlist=gen_yearlist('2013','2019')
#==============================================================================
def print_progress_bar(current,startnum,endnum):
    """
    功能：打印进度数值，每个10%打印一次，不换行
    """
    for i in [9,8,7,6,5,4,3,2,1]:
        if current == int((endnum - startnum)/10*i)+1: 
            print(str(i)+'0%',end=' '); break
        elif current == int((endnum - startnum)/100*i)+1: 
            print(str(i)+'%',end=' '); break
    if current == 2: print('0%',end=' ')

if __name__ =="__main__":
    startnum=2
    endnum=999
    L=range(2,999)
    for c in L: print_progress_bar(c,startnum,endnum)

#==============================================================================
def save_to_excel(df,filedir,excelfile,sheetname="Sheet1"):
    """
    函数功能：将df保存到Excel文件。
    如果目录不存在提示出错；如果Excel文件不存在则创建之文件并保存到指定的sheet；
    如果Excel文件存在但sheet不存在则增加sheet并保存df内容，原有sheet内容不变；
    如果Excel文件和sheet都存在则追加df内容到已有sheet的末尾
    输入参数：
    df: 数据框
    filedir: 目录
    excelfile: Excel文件名，不带目录，后缀为.xls或.xlsx
    sheetname：Excel文件中的sheet名
    输出：
    保存df到Excel文件
    无返回数据
    
    注意：如果df中含有以文本表示的数字，写入到Excel会被自动转换为数字类型保存。
    从Excel中读出后为数字类型，因此将会与df的类型不一致
    """

    #检查目录是否存在
    import os
    try:
        os.chdir(filedir)
    except:
        print("Error #1(save_to_excel): folder does not exist")        
        print("Information:",filedir)  
        return
                
    #取得df字段列表
    dflist=df.columns
    #合成完整的带目录的文件名
    filename=filedir+'/'+excelfile
    
    import pandas as pd
    try:
        file1=pd.ExcelFile(excelfile)
    except:
        #不存在excelfile文件，直接写入
        df.to_excel(filename,sheet_name=sheetname, \
                       header=True,encoding='utf-8')
        print("***Results saved in",filename,"@ sheet",sheetname)
        return
    else:
        #已存在excelfile文件，先将所有sheet的内容读出到dict中        
        dict=pd.read_excel(file1, None)
    file1.close()
    
    #获得所有sheet名字
    sheetlist=list(dict.keys())
    
    #检查新的sheet名字是否已存在
    try:
        pos=sheetlist.index(sheetname)
    except:
        #不存在重复
        dup=False
    else:
        #存在重复，合并内容
        dup=True
        #合并之前可能需要对df中以字符串表示的数字字段进行强制类型转换.astype('int')
        df1=dict[sheetlist[pos]][dflist]
        dfnew=pd.concat([df1,df],axis=0,ignore_index=True)        
        dict[sheetlist[pos]]=dfnew
    
    #将原有内容写回excelfile    
    result=pd.ExcelWriter(filename)
    for s in sheetlist:
        df1=dict[s][dflist]
        df1.to_excel(result,s,header=True,index=True,encoding='utf-8')
    #写入新内容
    if not dup: #sheetname未重复
        df.to_excel(result,sheetname,header=True,index=True,encoding='utf-8')
    try:
        result.save()
        result.close()
    except:
        print("Error #2(save_to_excel): writing file permission denied")
        print("Information:",filename)  
        return
    print("***Results saved in",filename,"@ sheet",sheetname)
    return       
#==============================================================================
def set_df_period(df,df_min,df_max):
    """
    功能： 去掉df中日期范围以外的记录
    """
    df1=df[df.index >= df_min]
    df2=df1[df1.index <= df_max]
    return df2

if __name__=='__main__':
    import siat.security_prices as ssp
    df=ssp.get_price('AAPL','2020-1-1','2020-1-31')    
    df_min,df_max=get_df_period(df)    
    df2=set_df_period(df,df_min,df_max)

#==============================================================================
def sigstars(p_value):
    """
    功能：将p_value转换成显著性的星星
    """
    if p_value >= 0.1: 
        stars="   "
        return stars
    if 0.1 > p_value >= 0.05:
        stars="*  "
        return stars
    if 0.05 > p_value >= 0.01:
        stars="** "
        return stars
    if 0.01 > p_value:
        stars="***"
        return stars

#==============================================================================

def regparms(results):
    """
    功能：将sm.OLS回归结果生成数据框，包括变量名称、系数数值、t值、p值和显著性星星
    """
    import pandas as pd
    #取系数
    params=results.params
    df_params=pd.DataFrame(params)
    df_params.columns=['coef']
    
    #取t值
    tvalues=results.tvalues
    df_tvalues=pd.DataFrame(tvalues)
    df_tvalues.columns=['t_values']

    #取p值
    pvalues=results.pvalues
    df_pvalues=pd.DataFrame(pvalues)
    df_pvalues.columns=['p_values']            

    #生成星星
    df_pvalues['sig']=df_pvalues['p_values'].apply(lambda x:sigstars(x))
    
    #合成
    parms1=pd.merge(df_params,df_tvalues, \
                    how='inner',left_index=True,right_index=True)
    parms2=pd.merge(parms1,df_pvalues, \
                    how='inner',left_index=True,right_index=True)

    return parms2
#==============================================================================
if __name__=='__main__':
    txt='QDII-指数'

def strlen(txt):
    """
    功能：计算中英文混合字符串的实际长度
    注意：有时不准
    """
    lenTxt = len(txt) 
    lenTxt_utf8 = len(txt.encode('utf-8')) 
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)    

    return size

#==============================================================================

def sort_pinyin(hanzi_list): 
    """
    功能：对列表中的中文字符串按照拼音升序排序
    """
    from pypinyin import lazy_pinyin       
    hanzi_list_pinyin=[]
    hanzi_list_pinyin_alias_dict={}
    
    for single_str in hanzi_list:
        py_r = lazy_pinyin(single_str)
        # print("整理下")
        single_str_py=''
        for py_list in py_r:
            single_str_py=single_str_py+py_list
        hanzi_list_pinyin.append(single_str_py)
        hanzi_list_pinyin_alias_dict[single_str_py]=single_str
    
    hanzi_list_pinyin.sort()
    sorted_hanzi_list=[]
    
    for single_str_py in hanzi_list_pinyin:
        sorted_hanzi_list.append(hanzi_list_pinyin_alias_dict[single_str_py])
    
    return sorted_hanzi_list


#==============================================================================
if __name__=='__main__':
    end_date='2021-11-18'
    pastyears=1

def get_start_date(end_date,pastyears=1):
    """
    输入参数：一个日期，年数
    输出参数：几年前的日期
    """

    import pandas as pd
    try:
        end_date=pd.to_datetime(end_date)
    except:
        print("  #Error(get_start_date): invalid date,",end_date)
        return None
    
    from datetime import datetime,timedelta
    start_date=datetime(end_date.year-pastyears,end_date.month,end_date.day)
    start_date2=start_date-timedelta(days=1)
    # 日期-1是为了保证计算收益率时得到足够的样本数量
    
    start_date3=str(start_date2.year)+'-'+str(start_date2.month)+'-'+str(start_date2.day)
    return start_date3
    
#==============================================================================
def get_ip():
    """
    功能：获得本机计算机名和IP地址    
    """
    #内网地址
    import socket
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    
    #公网地址

    return hostname,internal_ip

if __name__=='__main__':
    get_ip()
#==============================================================================
def check_date(adate):
    """
    功能：检查一个日期是否为有效日期
    输入参数：一个日期
    输出：合理日期为True，其他为False
    """
    #仅为测试使用，测试完毕需要注释掉
    #adate='2019-6-31'

    result=True
    import pandas as pd
    try:    
        bdate=pd.to_datetime(adate)
    except:
        print("  #Error(check_date): invalid date",adate)
        #print("Variable(s):",adate)
        result=False
        
    return result

if __name__ =="__main__":
    print(check_date('2019-6-31'))

#==============================================================================
def check_date2(adate):
    """
    功能：检查一个日期是否为有效日期，并转换标准的形式YYYY-MM-DD以便比较大小
    输入参数：一个日期
    输出：合理日期为True，其他为False
    """
    #仅为测试使用，测试完毕需要注释掉
    #adate='2019-6-31'

    result=True
    import pandas as pd
    try:    
        bdate=pd.to_datetime(adate)
    except:
        print("  #Error(check_date2): invalid date",adate)
        #print("Variable(s):",adate)
        result=False
        bdate=None
    
    if result:
        import datetime as dt
        fdate=dt.datetime.strftime(bdate,'%Y-%m-%d')
    else:
        fdate=adate
        
    return result,fdate

if __name__ =="__main__":
    adate='2023-1-25'
    print(check_date2('2019-6-31'))
    print(check_date2('2019-6-30'))
#==============================================================================
def check_start_end_dates(start,end):
    """
    功能：检查一个期间的开始/结束日期是否合理
    输入参数：开始和结束日期
    输出：合理为True，其他为False
    """
    #仅为测试使用，测试完毕需要注释掉
    #adate='2019-6-31'

    if not check_date(start):
        print("Error #1(check_start_end_dates): invalid start date")
        print("Variable(s):",start)
        return False

    if not check_date(end):
        print("Error #2(check_start_end_dates): invalid end date")
        print("Variable(s):",end)
        return False       
    
    if start > end:
        print("Error #3(check_start_end_dates): irrational start/end dates")
        print("Variable(s): from",start,"to",end)
        return False
        
    return True

if __name__ =="__main__":
    print(check_start_end_dates('2019-1-1','2019-8-18'))

#==============================================================================
if __name__ =="__main__":
    date1="2022-9-19"
    date2="2022-9-26"
    
def date_delta(date1,date2):
    """
    功能：计算两个日期之间相隔的天数
    """
    import pandas as pd    
    date1pd=pd.to_datetime(date1)
    date2pd=pd.to_datetime(date2)
    num=(date2pd - date1pd).days

    return num

if __name__ =="__main__":
    date_delta(date1,date2)
#==============================================================================

if __name__=='__main__':
    txt0="上市公司/家"        
        
def hzlen(txt0):
    """
    功能：计算含有汉字的字符串的长度
    """
    #strlen=int((len(txt.encode('utf-8')) - len(txt)) / 2 + len(txt))
    #strlen=int((len(txt.encode('gb18030')) - len(txt)) / 2 + len(txt))
    txt=str(txt0)
    
    import unicodedata
    #Unicode字符有不同的类别
    txtlist=list(unicodedata.category(c) for c in txt)
    strlen=0
    for t in txtlist:
        #类别Lo表示一个非拉丁文字
        if t == 'Lo':
            strlen=strlen+2
        else:
            strlen=strlen+1
    
    return strlen

#==============================================================================
def int10_to_date(int10):
    """
    功能：将10位数字的时间戳转换为日期。
    输入：10位数字的时间戳int10。
    返回：日期字符串。
    """
    import time
    tupTime = time.localtime(int10)
    y4m2d2 = time.strftime("%Y-%m-%d", tupTime)    
    return y4m2d2

if __name__ =="__main__":
    int10=9876543210
    print(int10_to_date(int10))    
#==============================================================================
def equalwidth(string,maxlen=20,extchar='.',endchar='：'):
    """
    输入：字符串，中英文混合
    输出：设定等宽度，自动补齐
    """
    reallen=hzlen(string)
    if maxlen < reallen:
        maxlen = reallen
    return string+extchar*(maxlen-reallen)+endchar

if __name__ =="__main__":
    equalwidth("中文1英文abc",maxlen=20)
#==============================================================================
if __name__ =="__main__":
    longlist=['豆粕', '玉米', '铁矿石', '棉花', '白糖', 'PTA', '甲醇', '橡胶', '沪铜', '黄金', '菜籽粕', '液化石油气', '动力煤']
    numperline=5
    beforehand=' '*4
    separator=' '
    
def printlist(longlist,numperline=5,beforehand='',separator=' '):
    """
    打印长列表，每numperline个一行，超过换行，分隔符为separator
    """
    listlen=len(longlist)
    if listlen==0:
        print("  #Warning(printlist): print list is empty")
        return
    
    counter=0
    lastone=longlist[-1]
    print(beforehand,end='')
    for l in longlist:
        if l == lastone:
            print(l)
            break
        
        counter=counter+1
        if counter <=numperline:
            print(l,end=separator)
        else:
            print('')
            print(beforehand,end='')
            counter=0
        
    print('')
    
    return        

#==============================================================================
if __name__=='__main__':
    ticker='600519.SS'
    ticker='AAPL'
    result,prefix,suffix=split_prefix_suffix(ticker)

def split_prefix_suffix(ticker):
    """
    将证券代码拆分为前后两部分
    """
    ticker=ticker.upper()
    result=False
    try:
        pos=ticker.index('.')
        prefix=ticker[:pos]
        suffix=ticker[pos+1:]
        result=True
    except:
        prefix=ticker
        suffix=''
        
    return result,prefix,suffix

if __name__=='__main__':
    split_prefix_suffix('600519.SS')
    split_prefix_suffix('600519.ss')
    split_prefix_suffix('AAPL')
    split_prefix_suffix('aapl')
#==================================================================================
if __name__=='__main__': 
    start='2022-1-1'
    end='2023-3-4'

shibor_period_list=['ON','1W','2W','1M','3M','6M','9M','1Y']

def get_shibor_rates_bs(start,end,rate_period='3M'):
    """
    功能：基于Baostock获得指定期间和期限的shibor利率
    start：开始日期
    end：结束日期
    rate_period：利率类型
    
    注意：这里得到的是年化利率，不带百分号，不是日利率！（日利率=年化利率/365）
    """
    #检查日期期间
    valid,start1,end1=check_period(start,end)
    if not valid:
        print("  #Error(get_shibor_rates): invalid date period from",start,"to",end)
        return None
    
    #检查利率类型
    if not (rate_period in shibor_period_list):
        print("  #Error(get_shibor_rates): unsupported rate period",rate_period)
        print("  Supported shibor rate periods:",shibor_period_list)
        return None
    
    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout
    
    import pandas as pd
    import baostock as bs
    # 登陆系统：不显示信息login success!
    with HiddenPrints():
        lg = bs.login()
    # 登陆失败处理
    if not (lg.error_code=='0'):
        print('  Baostock: login respond error_code:'+lg.error_code)
        print('  Baostock: login respond error_msg:'+lg.error_msg)
        return None

    # 获取银行间同业拆放利率
    rs = bs.query_shibor_data(start_date=start,end_date=end)
    if not (rs.error_code=='0'):
        print('  Baostock: query_shibor_data error_code:'+rs.error_code)
        print('  Baostock: query_shibor_data respond  error_msg:'+rs.error_msg)
        return None

    # 登出系统：不显示信息
    with HiddenPrints():
        lo=bs.logout()
    
    #提取数据，生成pandas格式
    rs_data=rs.data
    data_list = []
    for l in rs_data:
        data_list.append(l)

    rs_fields=rs.fields
    result = pd.DataFrame(data_list, columns=rs.fields)
    
    result['Date']=pd.to_datetime(result['date'])
    result.set_index(['Date'],inplace=True)
    
    result['rate']=round(result['shibor'+rate_period].astype('float')/100,5)
    result['period']=rate_period
    result1=result[['date','rate','period']]
    
    return result1
    
if __name__=='__main__': 
    get_shibor_rates_bs('2021-10-1','2021-11-28')   
    
#=============================================================================
if __name__=='__main__': 
    date='2023-12-15'
    rate_period='3M'
    rate_period='1Y'
    daysahead=360
    

def shibor_rate(date,rate_period='3M',daysahead=365*2):
    """
    获取指定日期和期限的shibor利率
    若无最新利率，则取最近日期的利率替代
    
    注意：这里得到的是年化利率，不带百分号，不是日利率！（日利率=年化利率/365）
    """    
    
    #检查日期有效性
    import datetime; todaydt = datetime.date.today().strftime('%Y-%m-%d')
    try:
        valid_date=check_date(date)
    except:
        date=todaydt
    if not valid_date:
        date=todaydt
        """
        print("  #Error(shibor_rate): invalid date",date)
        return None
        """
    start=date_adjust(date, adjust=-daysahead)
    
    rate_period=rate_period.upper()
    
    #检查利率期间有效性
    if not (rate_period in shibor_period_list):
        print("  #Error(shibor_rate): invalid shibor rate period",rate_period)
        print("  Supported shibor rate periods:",shibor_period_list)
        return None
    
    df=get_shibor_rates_bs(start,date,rate_period) 
    if df is None:
        rate=0
        return rate
    else:
        rate=float(df[-1:]['rate'].values[0])
    
    return rate
    
if __name__=='__main__': 
    shibor_rate('2021-11-19',rate_period='3M')
    shibor_rate('2021-11-19',rate_period='ON')
#==============================================================================        
if __name__=='__main__':
    start='2020-1-1'
    end='2023-3-4'
    term='1Y'
    
def treasury_yields_china(start,end,term='1Y'):
    """
    功能：抓取指定期间和期限的国债收益率
    
    注意：这里得到的是年化利率，不带百分号，不是日利率！（日利率=年化利率/365）
    """
    #检查日期期间
    valid,start1,end1=check_period(start,end)
    if not valid:
        print("  #Error(treasury_yields_china): invalid date period from",start,"to",end)
        return None
    
    #检查利率期间有效性
    term_list=['3M','6M','1Y','3Y','5Y','7Y','10Y','30Y']
    if not (term in term_list):
        print("  #Error(treasury_yields_china): invalid rate period",term)
        print("  Supported rate periods:",term_list)
        return None
    
    #抓取中债国债收益率
    import akshare as ak
    df = ak.bond_china_yield(start_date=start,end_date=end)
    if len(df)==0:
        return None
    
    df1=df[df['曲线名称']=='中债国债收益率曲线']
    df1.columns=['curve','date']+term_list
    df1.sort_values(by=['date'],ascending=['True'],inplace=True)
    
    df1['Date']=pd.to_datetime(df1['date'])
    df1.set_index(['Date'],inplace=True)    
    
    df1['rate']=df1[term]/100
    df1['period']=term
    df2=df1[['date','rate','period']]
    
    return df2

if __name__=='__main__':
    treasury_yields_china('2021-11-1','2021-11-28',term='1Y')
    
    
if __name__=='__main__':
    today='2023-3-4'
    term='1Y'
    daysahead=360
    
def treasury_yield_china(today,term='1Y',daysahead=360):
    """
    功能：抓取指定日期和期限的国债收益率
    
    注意：这里得到的是年化利率，不带百分号，不是日利率！（日利率=年化利率/365）
    """
    #检查日期
    valid=check_date(today)
    if not valid:
        print("  #Error(treasury_yield_china): invalid date",today)
        return None
    start = date_adjust(today, adjust=-daysahead)

    #检查利率期间有效性
    term_list=['3M','6M','1Y','3Y','5Y','7Y','10Y','30Y']
    if not (term in term_list):
        print("  #Error(treasury_yield_china): invalid rate period",term)
        print("  Supported rate periods:",term_list)
        return None
    
    rates=treasury_yields_china(start,today,term=term)
    rate=rates[-1:]['rate'].values[0]
        
    return rate
        
if __name__=='__main__':
    treasury_yield_china('2021-11-20',term='1Y')  
    treasury_yield_china('2021-11-18')
#==============================================================================
if __name__=='__main__':
    start='2019-1-1'
    end='2020-12-31'
    rate_period='1Y'
    rate_type='treasury'
    
def rf_daily_china(start,end,rate_period='1Y',rate_type='shibor'):
    """
    功能：抓取指定期间和期限的无风险利率
    
    注意：这里得到的是日利率，不带百分号，不是年化利率！（日利率=年化利率/365）
    """
    rate_type1=rate_type.upper()
    gotit=True
    
    if rate_type1=="TREASURY":
        if rate_period in ['3M','6M','1Y']:
            #使用国债收益率
            df=treasury_yields_china(start,end,rate_period)
        else:
            #使用shibor收益率
            df=get_shibor_rates_bs(start,end,rate_period)
    elif rate_type1=="SHIBOR":
        #使用shibor收益率
        df=get_shibor_rates_bs(start,end,rate_period)
        
        if df is None:
            #未能获取数据，Baostock获取的shibor利率一般滞后一个月左右
            gotit=False
        elif len(df)==0:
            gotit=False
        
        if not gotit:
            start1=date_adjust(start,adjust=-60)
            df=get_shibor_rates_bs(start1,end,rate_period)
    else:
        print("  #Warning(rf_daily_china): invalid rf rate type",rate_type)
        print("  Only support 2 types of rf: shibor rate, treasury yield")
        return None
    
    if df is None:
        gotit=False
    elif len(df)==0:
        gotit=False
    
    if not gotit:
        print("  #Warning(rf_daily_china): no rf data available between",start,end)
        return None
    
    #使用最近日期的利率填补空缺的日期
    latest_date=df['date'][-1:].values[0]
    lastest_rate=df['rate'][-1:].values[0]
    period=df['period'][-1:].values[0]

    collist=list(df)
    df_temp = pd.DataFrame(columns=collist)
    end_dt=pd.to_datetime(end)
    for i in range(100):
        date1=date_adjust(latest_date,adjust=i+1)
        date1_dt=pd.to_datetime(date1)
        if date1_dt <=end_dt:
            try:
                df_temp=df_temp.append({'date':date1,'rate':lastest_rate,'period':period},ignore_index=True)
            except:
                df_temp=df_temp._append({'date':date1,'rate':lastest_rate,'period':period},ignore_index=True)
        else:
            break
    
    df_temp['Date']=pd.to_datetime(df_temp['date'])
    df_temp.set_index(['Date'],inplace=True)    

    try:
        df1=df.append(df_temp)
    except:
        df1=df._append(df_temp)
    df1.sort_values(by=['date'],ascending=[True],inplace=True)
    
    df1['rf_daily']=df1['rate']/365
    
    return df1
    
if __name__=='__main__':
    rfd=rf_daily_china('2021-10-1','2021-11-28',rate_period='1Y',rate_type='shibor')
    rfd=rf_daily_china('2021-11-1','2021-11-28',rate_period='3M',rate_type='shibor')
    rfd=rf_daily_china('2021-11-1','2021-11-28',rate_period='1Y',rate_type='treasury')
    
#==============================================================================
if __name__=='__main__':
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio)
    leading_blanks=2

def print_tickerlist_sharelist(tickerlist,sharelist,leading_blanks=2):
    """
    功能：纵向打印投资组合的成分股和持股比例
    输入：
    tickerlist：成分股列表
    sharelist：持股份额列表
    leading_blanks：打印前导空格数
    """
    #检查成分股与持仓比例个数是否一致
    if not (len(tickerlist) == len(sharelist)):
        print("  #Error(): numbers of tickers and shares are not same")
        return
    
    #计算最长的代码长度，便于对齐
    max_ticker_len=0
    for t in tickerlist:
        tlen=len(t)
        #print(t,tlen)
        if tlen > max_ticker_len: #if的执行语句放在这里可能有bug
            max_ticker_len=tlen
    
    # 将原投资组合的权重存储为numpy数组类型，为了合成投资组合计算方便
    import numpy as np
    sharelist_array = np.array(sharelist)
    total_shares=sharelist_array.sum()
    weights=sharelist_array/total_shares 
    
    import pandas as pd
    df=pd.DataFrame(columns=['证券代码','证券名称','持仓比例'])
    for t in tickerlist:
        pos=tickerlist.index(t)
        tname=codetranslate(t)
        tweight=weights[pos]
        
        row=pd.Series({'证券代码':t,'证券名称':tname,'持仓比例':tweight})
        try:
            df=df.append(row,ignore_index=True)
        except:
            df=df._append(row,ignore_index=True)
    
    #按持仓比例降序
    df.sort_values(by='持仓比例',ascending=False,inplace=True)
    """
    #打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    print(df.to_string(index=False,header=False))
    """
    
    #打印
    df.reset_index(inplace=True) #必须，不然排序不起作用
    for i in range(len(df)):
        rows = df.loc[[i]]
        tcode=rows['证券代码'].values[0]
        tname=rows['证券名称'].values[0]
        tweight=rows['持仓比例'].values[0]
        print(' '*leading_blanks,tcode+' '*(max_ticker_len-len(tcode))+':',tname,'\b,',round(tweight,4)) 
        """
        values = rows.to_string(index=False,header=False)
        """
    
    return
    
if __name__=='__main__':
    print_tickerlist_sharelist(tickerlist,sharelist,leading_blanks=2)
#==============================================================================
if __name__=='__main__':
    current=0
    total=9
    steps=5
    leading_blanks=2

def print_progress_percent(current,total,steps=5,leading_blanks=2):
    """
    功能：打印进度百分比
    current：当前完成个数
    total：总个数
    steps：分成几个进度点显示
    leading_blanks：前置空格数
    """
    
    #间隔区间，最小为1
    fraction=int(total/steps)
    if fraction ==0:
        fraction=1
    
    if total < steps:
        steps=total
    
    #生成进度个数点位
    point_list=[]
    pct_list=[]
    for s in range(steps):
        #print("step=",s+1)
        point_list=point_list+[fraction*(s+1)-1]
        pct_list=pct_list+[str(int(100/steps*(s+1)))+'%']
    
    #当前完成第一个数时显示，其他时候不显示
    if current == 0: #range函数产生的第一个数是0
        print(' '*(leading_blanks - 1),"Progress...",end=' ')
    
    #打印当前进度百分比：到达点位时打印，否则无显示
    for p in point_list:
        if current == p:
            pos=point_list.index(p)
            pct=pct_list[pos]
            
            if pct=="100%":
                print("100% completing")
            else:
                print(pct,end=' ')
    
    return

if __name__=='__main__':
    for i in range(total): print_progress_percent(i,total,steps=5,leading_blanks=4)
    for i in range(total): print_progress_percent(i,total,steps=10,leading_blanks=4)

#==============================================================================
if __name__=='__main__':
    current='1'
    total_list=[str(x) for x in range(1000)]
    steps=5
    leading_blanks=4

def print_progress_percent2(current,total_list,steps=5,leading_blanks=4):
    """
    功能：打印进度百分比
    current：当前完成
    total：需要完成的列表
    steps：分成几个进度点显示
    leading_blanks：前置空格数
    """
    
    #间隔区间
    fraction=int(len(total_list)/steps)
    
    #生成进度个数点位
    point_list=[]
    pct_list=[]
    for s in range(steps):
        #print("step=",s+1)
        point_list=point_list+[fraction*(s+1)-1]
        pct_list=pct_list+[str(int(100/steps*(s+1)))+'%']
    
    #当前完成第一个数时显示，其他时候不显示
    pos=total_list.index(current)
    if pos == 0: #range函数产生的第一个数是0
        print(' '*(leading_blanks - 1),"Progress...",end=' ')
    
    #打印当前进度百分比：到达点位时打印，否则无显示
    for p in point_list:
        if pos == p:
            pos=point_list.index(p)
            pct=pct_list[pos]
            
            if pct=="100%":
                print("100% completing")
            else:
                print(pct,end=' ')
    
    return

if __name__=='__main__':
    for i in total_list: print_progress_percent2(i,total_list,steps=5,leading_blanks=4)
    for i in total_list: print_progress_percent2(i,total_list,steps=10,leading_blanks=4)

#==============================================================================
#==============================================================================
if __name__ == '__main__':
    numberPerLine=5
    leadingBlanks=2
    aList=['1', '2', '3', '4', '5', \
           '6', '7', '8', '9', '10', \
           '11', '12', '13', '14', '15', \
           '16', '17', '18', '19', '20', \
           '21', '22', '23', '24', '25', \
           '26', '27', '28']

def printInLine(aList,numberPerLine=5,leadingBlanks=2):
    """
    功能：将一个长列表等行分组打印
    """
    
    #分组
    groupedList=[]
    tmpList=[]
    n=0
    for a in aList:
        n=n+1
        if n <= numberPerLine:
            tmpList=tmpList+[a]
        else:
            groupedList=groupedList+[tmpList]
            n=1
            tmpList=[a]

    if len(tmpList) > 0:
        groupedList=groupedList+[tmpList]

    #按组打印
    for g in groupedList:
        if leadingBlanks >=1:
            print(' '*(leadingBlanks-1),*g,sep=' ')
        
    return
#==============================================================================
if __name__ == '__main__':
    numberPerLine=5
    leadingBlanks=2
    aList=['1', '2', '3', '4', '5', \
           '6', '7', '8', '9', '10', \
           '11', '12', '13', '14', '15', \
           '16', '17', '18', '19', '20', \
           '21', '22', '23', '24', '25', \
           '26', '27', '28']
    printInLine_md(aList,numberPerLine=8,colalign='center')

def printInLine_md(aList,numberPerLine=5,colalign='left'):
    """
    功能：将一个长列表等行分组打印，使用df.to_markdown方式打印，实现自动对齐
    aList：用于打印的数据列表
    numberPerLine：每行打印个数，默认5
    colalign：每个打印元素的对齐方式，默认左对齐'left'，居中'center'，右对齐'right'
    """
    
    #分组
    groupedList=[]
    tmpList=[]
    n=0
    for a in aList:
        n=n+1
        if n <= numberPerLine:
            tmpList=tmpList+[a]
        else:
            groupedList=groupedList+[tmpList]
            n=1
            tmpList=[a]

    if len(tmpList) > 0:
        groupedList=groupedList+[tmpList]
        
    #装入df
    cols=[' ']*numberPerLine
    import pandas as pd
    df=pd.DataFrame(groupedList,columns=cols)
    alignlist=[colalign]*numberPerLine
    print(df.to_markdown(index=False,tablefmt='plain',colalign=alignlist))

    return

#==============================================================================
def df_corr(df,fontsize=20):
    """
    功能：绘制df各个字段之间的Pearson相关系数的热力图
    """

    # 计算相关矩阵
    correlation_matrix = df.corr()
    
    # 导入seaborn
    import seaborn as sns
    # 创建热图
    sns.heatmap(correlation_matrix,annot=True,cmap="YlGnBu",linewidths=3,
            annot_kws={"size":fontsize})
    plt.title("皮尔逊相关系数示意图",fontsize=18)
    plt.ylabel("")
    
    footnote1=""
    import datetime as dt; stoday=dt.date.today()    
    footnote2="统计日期："+str(stoday)
    #plt.xlabel(footnote1+footnote2)
    #plt.xticks(rotation=30); plt.yticks(rotation=0) 
    plt.show()

    return    

if __name__=='__main__':
    Market={'Market':('US','^GSPC','我的组合001')}
#==============================================================================
#==============================================================================
def pandas2prettytable(df,titletxt,firstColSpecial=True,leftColAlign='l',otherColAlign='c',tabborder=False):
    """
    功能：将一个df转换为prettytable格式，打印，在Jupyter Notebook下整齐
    通用，但引入表格的字段不包括索引字段，利用prettytable插件
    注意：py文件最开始处要加上下面的语句
            from __future__ import unicode_literals
    """ 
    #列名列表
    col=list(df)
    
    # 第一列长度取齐处理
    if firstColSpecial:
        #第一列的最长长度
        firstcol=list(df[col[0]])
        maxlen=0
        for f in firstcol:
            flen=hzlen(f.strip())
            if flen > maxlen:
                maxlen=flen
        
        #将第一列内容的长度取齐
        df[col[0]]=df[col[0]].apply(lambda x:equalwidth(x.strip(),maxlen=maxlen,extchar=' ',endchar=' '))    
    
    itemlist=list(df)
    item1=itemlist[0]
    items_rest=itemlist[1:]
    
    from prettytable import PrettyTable
    import sys
    # 传入的字段名相当于表头
    tb = PrettyTable(itemlist, encoding=sys.stdout.encoding) 
    
    for i in range(0,len(df)): 
        tb.add_row(list(df.iloc[i]))
    
    # 第一个字段靠左
    tb.align[item1]=leftColAlign
    # 其余字段靠右
    for i in items_rest:
        tb.align[i]=otherColAlign
    
    # 边框设置：使用dir(tb)查看属性
    if not tabborder:
        # 无边框
        #tb.set_style(pt.PLAIN_COLUMNS) 
        # 空一行，分离标题行与表体
        #print()
        tb.junction_char=' '
        tb.horizontal_char=' '
        tb.vertical_char=' '
    
    # 设置标题
    tb.title=titletxt
        
    # 若有多个表格接连打印，可能发生串行。这时，第一个表格使用end=''，后面的不用即可
    print(tb)
    
    return

#==============================================================================
if __name__=='__main__':
    mstring="123王德宏456测试"
    mstring2number(mstring,numberType='int')
    mstring2number(mstring,numberType='float')

def mstring2number(mstring,numberType='int'):
    """
    功能：将含有非数字字符的数值字符串强行转化为数字
    numberType：输出类型，默认转换为整数类型int，亦可指定转换为浮点数类型float
    """
    digitlist=['0','1','2','3','4','5','6','7','8','9','.','-','+']
    for c in mstring:
        if not (c in digitlist):
            mstring=mstring.replace(c,'')
    
    if numberType == 'int':
        value=int(mstring)
    else:
        value=float(mstring)
        
    return value

#==============================================================================
if __name__=='__main__':
    time_priority_weighted_average(df,'蔚来汽车',decimals=4)

def time_priority_weighted_average(df,colname,decimals=4):
    """
    功能：对df中的colname列进行时间优先加权平均
    算法：将df索引列的datetime转换为8位数字，然后将每列的8位数字减去初始行的8位数字
    将其差作为权重
    """
    df['time_weight']=df.index.asi8
    df0=df.head(1)
    initial_weight=df0['time_weight'][0]
    df['relative_weight']=df['time_weight']-initial_weight
    
    # 双倍近期优先
    df['relative_weight2']=df['relative_weight'].apply(lambda x: x*2)
    
    import numpy as np
    try:
        tpwavg=np.average(df[colname],weights=df['relative_weight2'])
    except:
        return None
    
    return round(tpwavg,decimals)

#==============================================================================

if __name__=='__main__':
    tickers=['NIO','LI','XPEV','TSLA']
    df=compare_mrar(tickers,
                    rar_name='sharpe',
                    start='2022-1-1',end='2023-1-31',
                    market='US',market_index='^GSPC',
                    window=240,axhline_label='零线')    
    titletxt="This is the title text"
    footnote="This is the footnote"

def descriptive_statistics(df,titletxt,footnote,decimals=4,sortby='tpw_mean', \
                           recommend_only=False,trailing=20,trend_threshhold=0.01):
    """
    功能：进行描述性统计，并打印结果
    df的要求：
    索引列为datetime格式，不带时区
    各个列为比较对象，均为数值型，降序排列
    
    sortby='tpw_mean'：按照近期时间优先加权(time priority weighted)平均数排序
    recommend_only=False：是否仅打印推荐的证券
    """
    
    # 检查df
    if df is None:
        print("  #Error(descriptive_statistics): df is None")
        return
    if len(df) == 0:
        print("  #Error(descriptive_statistics): df is empty")
        return
    
    # 计算短期趋势
    df20=df[-trailing:]
    """
    df20ds=df20.describe()
    df20mean=df20ds[df20ds.index=='mean'].T
    
    df20tail=df20.tail(1).T
    df20tail.columns=['last']
    
    import pandas as pd
    df20trailing=pd.merge(df20tail,df20mean,left_index=True,right_index=True)
    df20trailing['trailing']=df20trailing['last']-df20trailing['mean']
    """
    ds=df.describe(include='all',percentiles=[.5])
    dst=ds.T   
    cols=['min','max','50%','mean','std']
    #cols=['min','max','50%','mean','trailing']
    
    dst['item']=dst.index
    #dstt=pd.merge(dst,df20trailing['trailing'],left_index=True,right_index=True)
    cols2=['item','min','max','50%','mean','std']
    #cols2=['item','min','max','50%','mean','trailing']
    
    #dst2=dstt[cols2]
    dst2=dst[cols2]
    for c in cols:
        dst2[c]=dst2[c].apply(lambda x: round(x,decimals))
    
    if sortby != 'tpw_mean': 
        if sortby=='median':
            sortby='50%'
        dst2.sort_values(by=sortby,ascending=False,inplace=True)

    cols2cn=['比较对象','最小值','最大值','中位数','平均值','标准差']
    #cols2cn=['比较对象','最小值','最大值','中位数','平均值','最新均值差']
    dst2.columns=cols2cn
    
    # 近期优先加权平均
    dst2['近期优先加权平均']=dst2['比较对象'].apply(lambda x:time_priority_weighted_average(df,x,4))
    if sortby == "tpw_mean":
        dst2.sort_values(by='近期优先加权平均',ascending=False,inplace=True)
    
    # 去掉带有缺失值的行
    #dst3=dst2.dropna()
    dst3=dst2
    #dst3=dst3[not (dst3['比较对象'] in ['time_weight','relative_weight']) ]
    dst3=dst3[(dst3['比较对象'] != 'time_weight') & (dst3['比较对象'] != 'relative_weight')]
    
    dst3.reset_index(drop=True,inplace=True)
    dst3.index=dst3.index+1
    
    # 趋势标记
    #dst3['期间趋势']='➠'
    #dst3['期间趋势']='➷'
    #dst3['期间趋势']=dst3.apply(lambda x: '➹' if (x['近期优先加权平均']>x['平均值']) & (x['近期优先加权平均']>x['中位数']) else x['期间趋势'],axis=1)
    #dst3['期间趋势']=dst3.apply(lambda x: '➷' if (x['近期优先加权平均']<x['平均值']) & (x['近期优先加权平均']<x['中位数']) else x['期间趋势'],axis=1)
    #dst3['期间趋势']=dst3['比较对象'].apply(lambda x:curve_trend_regress(df,x,trend_threshhold))
    dst3['期间趋势']=dst3['比较对象'].apply(lambda x:curve_trend_direct(df,x,trend_threshhold))

    #dst3['近期趋势']='➠'
    #dst3['近期趋势']='➷'
    #dst3['近期趋势']=dst3.apply(lambda x: '➹' if x['最新均值差'] > 0.0 else x['近期趋势'],axis=1)
    #dst3['期间趋势']=dst3.apply(lambda x: '➷' if x['最新均值差'] < 0.0 else x['近期趋势'],axis=1)
    #dst3['近期趋势']=dst3['比较对象'].apply(lambda x:curve_trend_direct(df20,x,trend_threshhold))
    #dst3['近期趋势']=dst3['比较对象'].apply(lambda x:curve_trend_regress(df20,x,trend_threshhold))
    dst3['近期趋势']=dst3['比较对象'].apply(lambda x:curve_trend_direct(df20,x,trend_threshhold))
    
    # 推荐标记
    dst3['推荐标记']=''
    """
    if sortby in ['tpw_mean','trailing']: #稳健推荐
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['近期优先加权平均']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['中位数']>0) & (x['平均值']>0) & (x['近期优先加权平均']>0) else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['近期优先加权平均'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['近期优先加权平均']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)
        
    elif sortby == 'min': #保守推荐
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['近期优先加权平均']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['最小值']>0) else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['最小值'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['最小值']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)
        
    elif sortby == 'mean': #进取推荐，均值
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['平均值']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['中位数']>0) & (x['推荐标记']=='✮') else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['平均值'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['平均值']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)
        
    elif sortby == 'median': #进取推荐，中位数
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['中位数']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['平均值']>0) & (x['推荐标记']=='✮') else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['中位数'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['中位数']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)   
    else:
        pass
    """
    if sortby in ['tpw_mean','trailing']: #稳健推荐
        dst3['推荐标记']=dst3.apply(lambda x: change_recommend_stars(x['推荐标记'],'+') if (x['近期优先加权平均']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: change_recommend_stars(x['推荐标记'],'+') if (x['中位数']>0) & (x['平均值']>0) & (x['中位数']>x['平均值']) else x['推荐标记'],axis=1)  
        
        dst3['推荐标记']=dst3.apply(lambda x: change_recommend_stars(x['推荐标记'],'+') if (x['中位数']>0) & (x['平均值']>0) & (x['近期优先加权平均']>max(x['中位数'],x['平均值'])) else x['推荐标记'],axis=1)
        """
        maxvalue=dst3['近期优先加权平均'].max()
        dst3['推荐标记']=dst3.apply(lambda x: change_recommend_stars(x['推荐标记'],'+') if (x['近期优先加权平均']==maxvalue) else x['推荐标记'],axis=1)
        """
    elif sortby == 'min': #保守推荐
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['近期优先加权平均']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['最小值']>0) else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['最小值'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['最小值']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)
        
    elif sortby == 'mean': #进取推荐，均值
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['平均值']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['中位数']>0) & (x['推荐标记']=='✮') else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['平均值'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['平均值']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)
        
    elif sortby == 'median': #进取推荐，中位数
        dst3['推荐标记']=dst3.apply(lambda x: '✮' if (x['中位数']>0) else x['推荐标记'],axis=1)
        
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮' if (x['平均值']>0) & (x['推荐标记']=='✮') else x['推荐标记'],axis=1)   
        
        maxvalue=dst3['中位数'].max()
        dst3['推荐标记']=dst3.apply(lambda x: '✮✮✮' if (x['中位数']==maxvalue) & (x['推荐标记']=='✮✮') else x['推荐标记'],axis=1)   
    else:
        pass
    
    
    # 下降趋势时，星星个数降一级，执行顺序不可颠倒
    dst4=dst3
    
    # 减少星星的情形
    #droplist1=['➷','➠']
    droplist1=['➷']
    droplist2=['➷']
    dst4['推荐标记']=dst4.apply(lambda x: change_recommend_stars(x['推荐标记'],'-') if (x['期间趋势'] in droplist1) else x['推荐标记'],axis=1)
    dst4['推荐标记']=dst4.apply(lambda x: change_recommend_stars(x['推荐标记'],'-') if (x['近期趋势'] in droplist2) else x['推荐标记'],axis=1)
    """
    # 一颗星颗星-->无星
    dst4['推荐标记']=dst4.apply(lambda x: '' if (x['推荐标记']=='✮') & (x['期间趋势'] in droplist) else x['推荐标记'],axis=1) 
    dst4['推荐标记']=dst4.apply(lambda x: '' if (x['推荐标记']=='✮') & (x['近期趋势'] in droplist) else x['推荐标记'],axis=1)   
    
    
    # 两颗星颗星-->一颗星
    dst4['推荐标记']=dst4.apply(lambda x: '✮' if (x['推荐标记']=='✮✮') & (x['期间趋势'] in droplist) else x['推荐标记'],axis=1)
    dst4['推荐标记']=dst4.apply(lambda x: '✮' if (x['推荐标记']=='✮✮') & (x['近期趋势'] in droplist) else x['推荐标记'],axis=1)   
    
    # 三颗星-->两颗星✮
    #dst4['推荐标记']=dst4.apply(lambda x: '✮✮✩' if (x['推荐标记']=='✮✮✮') & (x['趋势']=='➷') else x['推荐标记'],axis=1)
    dst4['推荐标记']=dst4.apply(lambda x: '✮✮' if (x['推荐标记']=='✮✮✮') & (x['期间趋势'] in droplist) else x['推荐标记'],axis=1)
    dst4['推荐标记']=dst4.apply(lambda x: '✮✮' if (x['推荐标记']=='✮✮✮') & (x['近期趋势'] in droplist) else x['推荐标记'],axis=1)
    """
    
    # 上升趋势时，星星个数加一级，执行顺序不可颠倒
    dst4['推荐标记']=dst4.apply(lambda x: change_recommend_stars(x['推荐标记'],'+') if (x['期间趋势']=='➹') & (x['近期趋势']=='➹') else x['推荐标记'],axis=1)
    
    """
    # 两颗星颗星-->三颗星
    dst4['推荐标记']=dst4.apply(lambda x: '✮✮✮' if (x['推荐标记']=='✮✮') & (x['期间趋势']=='➹') else x['推荐标记'],axis=1) 
    dst4['推荐标记']=dst4.apply(lambda x: '✮✮✮' if (x['推荐标记']=='✮✮') & (x['近期趋势']=='➹') else x['推荐标记'],axis=1)   
    
    # 一颗星颗星-->两颗星
    dst4['推荐标记']=dst4.apply(lambda x: '✮✮' if (x['推荐标记']=='✮') & (x['期间趋势']=='➹') else x['推荐标记'],axis=1) 
    dst4['推荐标记']=dst4.apply(lambda x: '✮✮' if (x['推荐标记']=='✮') & (x['近期趋势']=='➹') else x['推荐标记'],axis=1)   
    
    # 零颗星-->一颗星
    dst4['推荐标记']=dst4.apply(lambda x: '✮' if (x['推荐标记']=='') & (x['期间趋势']=='➹') & (x['近期趋势']=='➹') else x['推荐标记'],axis=1) 
    dst4['推荐标记']=dst4.apply(lambda x: '✮' if (x['推荐标记']=='') & (x['期间趋势']=='➹') else x['推荐标记'],axis=1) 
    dst4['推荐标记']=dst4.apply(lambda x: '✮' if (x['推荐标记']=='') & (x['近期趋势']=='➹') else x['推荐标记'],axis=1)  
    """
    
    # 重排序：按照星星个数+数值，降序
    dst5=dst4
    if sortby == "tpw_mean":
        dst5.sort_values(by=['推荐标记','近期优先加权平均'],ascending=[False,False],inplace=True)
        #dst5.sort_values(by=['推荐标记','近期优先加权平均'],ascending=False,inplace=True)
    elif sortby == "min":
        dst5.sort_values(by=['推荐标记','最小值'],ascending=[False,False],inplace=True)
    elif sortby == "mean":
        dst5.sort_values(by=['推荐标记','平均值'],ascending=[False,False],inplace=True)
    elif sortby == "median":
        dst5.sort_values(by=['推荐标记','中位数'],ascending=[False,False],inplace=True)
    elif sortby == "trailing":
        dst5.sort_values(by=['推荐标记','最新均值差'],ascending=[False,False],inplace=True)
    else:
        pass
    
    #是否过滤无推荐标志的证券，防止过多无推荐标志的记录使得打印列表过长
    if recommend_only:
        dst6=dst5[dst5['推荐标记'] != '']
        dst_num=len(dst6)
        #若无推荐标志也要显示头十个
        if dst_num < 10:
            dst6=dst5.head(10)
        else:
            dst6=dst5.head(dst_num+3)
    else:
        dst6=dst5
    
    dst6.reset_index(drop=True,inplace=True)
    dst6.index=dst6.index+1
    
    print("\n"+titletxt+"\n")
    #alignlist=['right','left']+['center']*(len(list(dst4))-1)
    alignlist=['right','left']+['center']*(len(list(dst6))-3)+['center','left']
    try:   
        print(dst6.to_markdown(index=True,tablefmt='plain',colalign=alignlist))
    except:
        #解决汉字编码gbk出错问题
        dst7=dst6.to_markdown(index=True,tablefmt='plain',colalign=alignlist)
        dst8=dst7.encode("utf-8",errors="strict")
        print(dst8)
    
    print("\n"+footnote)
    
    return dst5


#==============================================================================
if __name__=='__main__':
    alist=['NIO','LI','XPEV','TSLA']
    print_list(alist)

def print_list(alist,leading_blanks=1):
    """
    功能：打印一个字符串列表，不带引号，节省空间
    """
    print(' '*leading_blanks,end='')
    
    for i in alist:
        print(i,end=' ')
    print('\n')
    
    return
#==============================================================================
# FUNCTION TO REMOVE TIMEZONE
def remove_timezone(dt):
   
    # HERE `dt` is a python datetime
    # object that used .replace() method
    return dt.replace(tzinfo=None)
#==============================================================================
def remove_df_index_timezone(df):
    df['timestamp']=df.index
    df['timestamp'] = df['timestamp'].apply(remove_timezone)
    df.index=df['timestamp']
    del df['timestamp']
    
    return df
#==============================================================================
if __name__=='__main__':
    ltext='景顺长城沪深300指数增强A,景顺长城量化精选股票,景顺长城量化新动力股票,景顺长城量化平衡混合'

def print_long_text(ltext,separators=[',','，'],numberPerLine=4,colalign='left'):
    """
    功能：分行打印有规律的长字符串，每行打印numPerLine，分隔符列表为separators
    """
    # 分隔符合成
    reSeparator=''
    for s in separators:
        reSeparator=reSeparator+s+'|'
    reSLen=len(reSeparator) 
    reSeparator=reSeparator[:-1]           
    
    # 分割长字符串，形成列表
    import re
    aList=re.split(reSeparator,ltext)
    aListLen=len(aList)
    printInLine_md(aList,numberPerLine=numberPerLine,colalign=colalign)
    
    return aListLen
    
#==============================================================================
if __name__=='__main__':
    printInMarkdown(df)

def printInMarkdown(df,titletxt='',footnote='', \
                    firstAlign='center',restAlign='center'):
    """
    功能：使用markdown格式打印df
    """
    colList=list(df)
    colNum=len(colList)

    # 打印标题
    if not titletxt == '':
        print(' ')
        print(titletxt,'\n')
    else:
        print(' ')
    
    # 打印表体
    alignList=[firstAlign]+[restAlign]*(colNum-1)
    print(df.to_markdown(index=False,tablefmt='plain',colalign=alignList))
    
    # 打印尾注
    if not footnote == '':
        print('\n',footnote)
    
    return
#==============================================================================
if __name__=='__main__':
    df=security_price("600519.SS","2023-1-1","2023-6-30")
    col='Close'
    threshhold=0.1
    curve_trend_regress(df,col,threshhold=0.1)
    
    df=security_price("AAPL","2023-1-1","2023-6-30")
    curve_trend_regress(df,col,threshhold=0.1)    
    
    df=security_price("AAPL","2023-1-1","2023-1-10")
    curve_trend_regress(df,col,threshhold=0.1) 

    
def curve_trend_regress(df,col,threshhold=0.0001):
    """
    功能：回归简单方程y=a+b*x，并判断系数b的显著性星星。目的为判断曲线走势
    
    输入项：
    df: 数据框，假设其索引为日期项，且已升序排列
    col: 因变量，检查该变量的走势，向上，向下，or 不明显（无显著性星星）
    
    返回值：
    '？'：回归不成功
    '➠'：回归结果不显著或斜率接近零(其绝对值小于threshhold)
    '➷'：斜率为负数且其绝对值不小于threshhold且显著
    '➹'：斜率为正数且其绝对值不小于threshhold且显著
    """    
    # 检查df是否为空
    if df is None:
        return ' '
    if len(df)==0:
        return ' '
    
    # 按照索引升序排列，以防万一
    df1=df.copy()
    df1.sort_index(ascending=True,inplace=True)
    df1['id']=range(len(df1))
    
    from scipy import stats
    try:
        output=stats.linregress(df1['id'],df1[col])
        (b,a,r_value,p_value,std_err)=output
    except:
        # 处理可能的空值
        df1.fillna(method='ffill',inplace=True)
        df1.fillna(method='bfill',inplace=True)
        try:
            output=stats.linregress(df1['id'],df1[col])
            (b,a,r_value,p_value,std_err)=output
        except:
            return ' '
    
    # 生成显著性星星
    stars=sigstars(p_value)
    
    # 判断斜率方向
    b_abs=abs(b)
    result='➠'
    #if b_abs >= threshhold and b > 0 and '*' in stars:
    if b_abs >= threshhold and b > 0:    
        result='➹'
    #if b_abs >= threshhold and b < 0 and '*' in stars:
    if b_abs >= threshhold and b < 0:    
        result='➷'
    
    return result

def curve_trend_direct(df,col,threshhold=0.0001):
    """
    功能：直接对比首尾值大小。目的为判断曲线走势
    
    输入项：
    df: 数据框，假设其索引为日期项，且已升序排列
    col: 考察变量，检查该变量的走势，向上，向下，or 不明显（无显著性星星）
    
    返回值：尾值-首值
    '➠'：差接近零(其绝对值小于threshhold)
    '➷'：差为负数且其绝对值不小于threshhold
    '➹'：差为正数且其绝对值不小于threshhold
    """    
    # 检查df是否为空
    if df is None:
        return ' '
    if len(df)==0:
        return ' '
    
    # 按照索引升序排列，以防万一
    df1=df.copy()
    df1.sort_index(ascending=True,inplace=True)
    first_value=df1.head(1)[col].values[0]
    last_value=df1.tail(1)[col].values[0]
    diff=last_value - first_value
    diff_abs=abs(diff)
    
    # 判断斜率方向
    result='➠'
    if diff_abs >= threshhold and diff > 0:    
        result='➹'
    if diff_abs >= threshhold and diff < 0:    
        result='➷'
    
    return result    
#==============================================================================
if __name__=='__main__':
    stars_current=''
    change_recommend_stars(stars_current,change='+')
    change_recommend_stars(stars_current,change='-')
    
    stars_current='✮'
    change_recommend_stars(stars_current,change='+')
    change_recommend_stars(stars_current,change='-')
    
    stars_current='✮✮'
    change_recommend_stars(stars_current,change='+')
    change_recommend_stars(stars_current,change='-')
    
    stars_current='✮✮✮'
    change_recommend_stars(stars_current,change='+')
    change_recommend_stars(stars_current,change='-')
    
    
def change_recommend_stars(stars_current,change='+'):
    """
    功能：增减推荐的星星个数
    """   
    stars0=''
    stars1='✮'
    stars2='✮✮'
    stars3='✮✮✮'
    
    # 计算当前的星星个数
    if stars_current==stars0:
        num=0
    elif stars_current==stars1:
        num=1
    elif stars_current==stars2:
        num=2
    elif stars_current==stars3:
        num=3
    else:
        num=3
        
    if change == '+':
        if stars_current==stars0:
            stars_new=stars1
        elif stars_current==stars1:
            stars_new=stars2
        elif stars_current==stars2:
            stars_new=stars3
        elif stars_current==stars3:
            stars_new=stars3
        else:
            stars_new=stars3
        
    if change == '-':
        if stars_current==stars0:
            stars_new=stars0
        elif stars_current==stars1:
            stars_new=stars0
        elif stars_current==stars2:
            stars_new=stars1
        elif stars_current==stars3:
            stars_new=stars2
        else:
            stars_new=stars2   
            
    return stars_new
    


#==============================================================================
if __name__=='__main__':
    symbol='---'
    exclude_collist=['c1']
    
    import pandas as pd
    df=pd.DataFrame({'c1':[10,11,12],'c2':['---',110,'---'],'c3':['---',1100,'---']})
    df_filter_row(df,exclude_collist=['c1'],symbol='---')
    
def df_filter_row(df,exclude_collist=[],symbol=''):
    """
    功能：删除df中的全部行，如果该行除去exclude_collist外其全部列的1值均为symbol
    """
    # 若为空直接返回
    if len(df)==0:
        return df
    
    # 找出需要判断的列列表
    collist=list(df)
    for e in exclude_collist:
        collist.remove(e)
    
    # 逐行打是否为symbol标记
    df2=df.copy()
    df2['EmptyRow']=True    # 假定所有行都符合条件
    for index,row in df2.iterrows():
        for c in collist:
            #if row[c] not in [symbol,' ',0]:
            if row[c] not in [symbol]:
                df2.loc[index,'EmptyRow']=False

    # 删除符合条件的行                
    df3=df2[df2['EmptyRow']==False]
    df3.drop('EmptyRow',axis=1,inplace=True)
    
    return df3
        
        

#==============================================================================
if __name__=='__main__':
    a=65
    a=6.6000000000000005
    decimal=4
    sround(a,decimal=4)
    
def sround(a,decimal=4):
    """
    功能：解决round小数位偶尔无法截取问题，采取转字符串截取再转数值的方法
    注意：适合哪些偶尔但顽固出现小数位无法截取成功的难题
    """
    a1=str(a)
    a1list=a1.split('.')
    if len(a1list)==1:#无小数点，无需round
        return a
    
    a2=a1list[1]  
    a3=a2[:decimal]
    a4=a1list[0]+'.'+a3
    a5=float(a4)
    
    return a5

    
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================

