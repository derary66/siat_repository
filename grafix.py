# -*- coding: utf-8 -*-
"""
本模块功能：绘制折线图，单线，双线，多线
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年9月16日
最新修订日期：2020年9月16日
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
from siat.common import *
from siat.translate import *
import pandas as pd
#==============================================================================
import matplotlib.pyplot as plt

#统一设定绘制的图片大小：数值为英寸，1英寸=100像素
plt.rcParams['figure.figsize']=(12.8,7.2)
plt.rcParams['figure.dpi']=300
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize']=11 #横轴字体大小
plt.rcParams['ytick.labelsize']=11 #纵轴字体大小

title_txt_size=16
ylabel_txt_size=14
xlabel_txt_size=14
legend_txt_size=14

#设置绘图风格：网格虚线
plt.rcParams['axes.grid']=True
#plt.rcParams['grid.color']='steelblue'
#plt.rcParams['grid.linestyle']='dashed'
#plt.rcParams['grid.linewidth']=0.5
#plt.rcParams['axes.facecolor']='whitesmoke'

#设置刻度线风格：in，out，inout
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向外
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内外

#处理绘图汉字乱码问题
import sys; czxt=sys.platform
if czxt in ['win32','win64']:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    mpfrc={'font.family': 'SimHei'}

if czxt in ['darwin']: #MacOSX
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family': 'Heiti TC'}

if czxt in ['linux']: #website Jupyter
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family':'Heiti TC'}

# 解决保存图像时'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 
#==============================================================================
def plot_line(df0,colname,collabel,ylabeltxt,titletxt,footnote,datatag=False, \
              power=0,zeroline=False,resample_freq='H',loc='best', \
              date_range=False,date_freq=False,date_fmt='%Y-%m-%d'):
    """
    功能：绘制折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：数据表df，数据表中的列名colname，列名的标签collabel；y轴标签ylabeltxt；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：折线图
    返回值：无
    注意：需要日期类型作为df索引
    """
    #空值判断
    if len(df0) ==0:
        print ("  #Warning(plot_line): no data to plot.")
        return
    
    #插值平滑
    try:
        df0x=df0[[colname]].astype('float')
        df=df_smooth_manual(df0x,resample_freq=resample_freq)
    except:
        df=df0
    
    #先绘制折线图
    """
    plt.plot(df.index,df[colname],'-',label=collabel, \
             linestyle='-',color='blue', linewidth=1, \
                 marker='o',markersize=2)
    """

    import matplotlib.dates as mdate
    date_start=df.index[0]
    date_end=df.index[-1]
    ax=plt.gca()       
    
    if date_range and not date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))

    plt.plot(df.index,df[colname],'-',label=collabel, \
             linestyle='-',color='blue', linewidth=2)
    #绘制数据标签
    if datatag:
        for x, y in zip(df.index, df[colname]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
    
    #是否绘制水平线
    #if zeroline and (min(df[colname]) < 0):
    if zeroline:
        if isinstance(zeroline,bool):
            hline=0
        elif isinstance(zeroline,float):
            hline=zeroline
        elif isinstance(zeroline,int):
            hline=zeroline
        else:
            hline=0
        plt.axhline(y=hline,ls=":",c="black",linewidth=2)
        
    #绘制趋势线
    #print("--Debug(plot_line): power=",power)
    if power > 0:
        lang=check_language()
        #trend_txt='趋势线'
        trend_txt=''
        if lang == 'English':
            trend_txt='Trend line'           
        
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df['id']=range(len(df))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df.id, df[colname], power)
            f = np.poly1d(parameter)
            plt.plot(df.index, f(df.id),"r--", label=trend_txt,linewidth=1)
        except: 
            print("  Warning(plot_line): failed to converge trend line, try a smaller power.")
    
    plt.legend(loc=loc,fontsize=legend_txt_size)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.ylabel(ylabeltxt,fontsize=ylabel_txt_size)
    plt.xlabel(footnote,fontsize=xlabel_txt_size)
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    
    plt.show()
    plt.close()
    
    return

if __name__ =="__main__":
    plot_line(df,'Close',"收盘价","价格","万科股票","数据来源：新浪/stooq",power=4)

#==============================================================================
if __name__ =="__main__":
    power=0
    datatag1=False
    datatag2=False
    yscalemax=5
    zeroline=False
    twinx=False
    yline=999
    xline=999
    resample_freq='H'

def plot_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=0,datatag1=False,datatag2=False,yscalemax=5, \
               zeroline=False,twinx=False,yline=999,xline=999, \
               resample_freq='H',loc1='best',loc2='best', \
               color1='red',color2='blue'):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：默认绘制同轴折线图，若twinx=True则绘制双轴折线图
    返回值：无
    注意：需要日期类型作为df索引
    """
    #空值判断
    if len(df1) ==0:
        print ("  #Warning(plot_line2): no data to plot df1.")
    if len(df2) ==0:
        print ("  #Warning(plot_line2): no data to plot df2.")
    if (len(df1) ==0) and (len(df2) ==0):
        return
    
    if not twinx:            
        plot_line2_coaxial(df1,ticker1,colname1,label1, \
                           df2,ticker2,colname2,label2, \
                ylabeltxt,titletxt,footnote,power,datatag1,datatag2,zeroline, \
                yline,xline,resample_freq=resample_freq, \
                    loc1=loc1,loc2=loc2, \
                    color1=color1,color2=color2)
    else:
        plot_line2_twinx(df1,ticker1,colname1,label1, \
                         df2,ticker2,colname2,label2, \
                         titletxt,footnote,power,datatag1,datatag2, \
                         resample_freq=resample_freq, \
                             loc1=loc1,loc2=loc2, \
                             color1=color1,color2=color2)
    return


#==============================================================================
def plot2_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=0,datatag1=False,datatag2=False,yscalemax=5, \
               zeroline=False,twinx=False,yline=999,xline=999, \
               resample_freq='H',loc1='best',loc2='best', \
               date_range=False,date_freq=False,date_fmt='%Y-%m-%d', \
               color1='red',color2='blue'):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：默认绘制同轴折线图，若twinx=True则绘制双轴折线图
    返回值：无
    注意：需要日期类型作为df索引
    
    date_range：表示绘图横轴是否需要尽量绘制开始和结束日期
    date_freq：定义绘图横轴的日期间隔，False表示自动间隔，'1Y'表示以1年为单位间隔,
               '1M'表示间隔一个月，'3M'表示间隔3个月等
    date_fmt：定义绘图横轴日期的格式，'%Y-%m-%d'表示YYYY-mm-dd，'%Y-%m'表示YYYY-mm，
               '%Y'表示YYYY
    """
    #空值判断
    if len(df1) ==0:
        print ("  #Warning(plot_line2): no data to plot df1.")
    if len(df2) ==0:
        print ("  #Warning(plot_line2): no data to plot df2.")
    if (len(df1) ==0) and (len(df2) ==0):
        return
    
    if not twinx:            
        plot_line2_coaxial2(df1,ticker1,colname1,label1, \
                           df2,ticker2,colname2,label2, \
                ylabeltxt,titletxt,footnote,power,datatag1,datatag2,zeroline, \
                yline,xline,resample_freq=resample_freq, \
                loc1=loc1,loc2=loc2, \
                date_range=date_range,date_freq=date_freq,date_fmt=date_fmt, \
                color1=color1,color2=color2)
    else:
        plot_line2_twinx2(df1,ticker1,colname1,label1, \
                         df2,ticker2,colname2,label2, \
                         titletxt,footnote,power,datatag1,datatag2, \
                         resample_freq=resample_freq, \
                         loc1=loc1,loc2=loc2, \
                         date_range=date_range,date_freq=date_freq,date_fmt=date_fmt, \
                         color1=color1,color2=color2)
    return


#==============================================================================


def plot_line2_coaxial(df01,ticker1,colname1,label1, \
                       df02,ticker2,colname2,label2, \
                    ylabeltxt,titletxt,footnote, \
                    power=0,datatag1=False,datatag2=False,zeroline=False, \
                    yline=999,xline=999,resample_freq='H', \
                        loc1='best',loc2='best', \
                        color1='red',color2='blue'):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制同轴折线图
    返回值：无
    注意：需要日期类型作为df索引
    """

    #插值平滑
    try:
        df01x=df01[[colname1]].astype('float')
        df1=df_smooth_manual(df01x,resample_freq=resample_freq)
    except:
        df1=df01
    try:
        df02x=df02[[colname2]].astype('float')
        df2=df_smooth_manual(df02x,resample_freq=resample_freq)
    except:
        df2=df02
    #证券1：先绘制折线图
    
    if ticker1 == '':
        label1txt=label1
    else:
        if label1 == '':
            label1txt=codetranslate(ticker1)
        else:
            label1txt=codetranslate(ticker1)+'('+label1+')'    
    
    plt.plot(df1.index,df1[colname1],'-',label=label1txt, \
             linestyle='-',linewidth=2.5,color=color1)
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        

    #是否绘制水平0线
    if zeroline and ((min(df1[colname1]) < 0) or (min(df2[colname2]) < 0)):
        plt.axhline(y=0,ls=":",c="black",linewidth=2)

    #是否绘制水平线
    if yline != 999:
        plt.axhline(y=yline,ls=":",c="black",linewidth=2)        

    #是否绘制垂直线
    if xline != 999:
        plt.axvline(x=xline,ls=":",c="black",linewidth=1)   
    
    #绘证券1：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'    
            
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df1['id']=range(len(df1))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df1.id, df1[colname1], power)
            f = np.poly1d(parameter)
            
            if ticker1 == '':
                label1txt=''
            else:
                label1txt=codetranslate(ticker1)+"("+trend_txt+")"            
                    
            #plt.plot(df1.index, f(df1.id),"g--", label=label1txt,linewidth=1)
            plt.plot(df1.index, f(df1.id),"g--", label='',linewidth=1)
        except: pass
    
    #证券2：先绘制折线图
    if ticker2 == '':
        label2txt=label2
    else:
        if label2 == '':
            label2txt=codetranslate(ticker2)
        else:
            label2txt=codetranslate(ticker2)+'('+label2+')'    
    
    plt.plot(df2.index,df2[colname2],'-',label=label2txt, \
             linestyle='-.',linewidth=2.5,color=color2)
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
        
    #绘证券2：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'    
            
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df2['id']=range(len(df2))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df2.id, df2[colname2], power)
            f = np.poly1d(parameter)
            
            if ticker2 == '':
                label2txt=''
            else:
                label2txt=codetranslate(ticker2)+"("+trend_txt+")"            
                    
            #plt.plot(df2.index, f(df2.id),"r--", label=label2txt,linewidth=1)
            plt.plot(df2.index, f(df2.id),"r--", label='',linewidth=1)
        except: pass
    
    # 同轴绘图时，loc1/loc2未用上！
    plt.legend(loc=loc1,fontsize=legend_txt_size)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.ylabel(ylabeltxt,fontsize=ylabel_txt_size)
    plt.xlabel(footnote,fontsize=xlabel_txt_size)
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    plt.show()
    plt.close()
    
    return

if __name__ =="__main__":
    df1 = get_price('000002.SZ', '2020-1-1', '2020-3-16')
    df2 = get_price('600266.SS', '2020-1-1', '2020-3-16')
    ticker1='000002.SZ'; ticker2='600266.SS'
    colname1='Close'; colname2='Close'
    label1="收盘价"; label2="收盘价"
    ylabeltxt="价格"
    plot_line2_coaxial(df1,'000002.SZ','High','最高价', \
        df1,'000002.SZ','Low','最低价',"价格", \
        "证券价格走势对比图","数据来源：新浪/stooq")
    plot_line2_coaxial(df1,'000002.SZ','Open','开盘价', \
        df1,'000002.SZ','Close','收盘价',"价格", \
        "证券价格走势对比图","数据来源：新浪/stooq")

    plot_line2_coaxial(df2,'600266.SS','Open','开盘价', \
        df2,'600266.SS','Close','收盘价',"价格", \
        "证券价格走势对比图","数据来源：新浪/stooq")

#==============================================================================
def plot_line2_coaxial2(df01,ticker1,colname1,label1, \
                       df02,ticker2,colname2,label2, \
                       ylabeltxt,titletxt,footnote, \
                       power=0,datatag1=False,datatag2=False,zeroline=False, \
                       yline=999,xline=999,resample_freq='H', \
                       loc1='best',loc2='best', \
                       date_range=False,date_freq=False,date_fmt='%Y-%m-%d', \
                       color1='red',color2='blue'):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制同轴折线图
    返回值：无
    注意：需要日期类型作为df索引
    """

    #插值平滑
    try:
        df01x=df01[[colname1]].astype('float')
        df1=df_smooth_manual(df01x,resample_freq=resample_freq)
    except:
        df1=df01
    try:
        df02x=df02[[colname2]].astype('float')
        df2=df_smooth_manual(df02x,resample_freq=resample_freq)
    except:
        df2=df02
    #证券1：先绘制折线图
    
    if ticker1 == '':
        label1txt=label1
    else:
        if label1 == '':
            label1txt=codetranslate(ticker1)
        else:
            label1txt=codetranslate(ticker1)+'('+label1+')'    

    import matplotlib.dates as mdate
    ax=plt.gca()    
    date_start=df1.index[0]
    date_end=df1.index[-1]
    if date_range and not date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))    

    plt.plot(df1.index,df1[colname1],'-',label=label1txt, \
             linestyle='-',linewidth=2.5,color=color1)
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        

    #是否绘制水平0线
    if zeroline and ((min(df1[colname1]) < 0) or (min(df2[colname2]) < 0)):
        plt.axhline(y=0,ls=":",c="black",linewidth=2.5)

    #是否绘制水平线
    if yline != 999:
        plt.axhline(y=yline,ls=":",c="black",linewidth=2.5)        

    #是否绘制垂直线
    if xline != 999:
        plt.axvline(x=xline,ls=":",c="black",linewidth=2.5)   
    
    #绘证券1：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'        
        
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df1['id']=range(len(df1))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df1.id, df1[colname1], power)
            f = np.poly1d(parameter)
            
            if ticker1 == '':
                label1txt=''
            else:
                label1txt=codetranslate(ticker1)+"("+trend_txt+")"            
            plt.plot(df1.index, f(df1.id),"g--", label=label1txt,linewidth=1)
        except: pass
    
    #证券2：先绘制折线图
    if ticker2 == '':
        label2txt=label2
    else:
        if label2 == '':
            label2txt=codetranslate(ticker2)
        else:
            label2txt=codetranslate(ticker2)+'('+label2+')'    

    date_start=df2.index[0]
    date_end=df2.index[-1]
    if date_range and not date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))

    plt.plot(df2.index,df2[colname2],'-',label=label2txt, \
             linestyle='-.',linewidth=2.5,color=color2)
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
        
    #绘证券2：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'        
        
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df2['id']=range(len(df2))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df2.id, df2[colname2], power)
            f = np.poly1d(parameter)
            
            if ticker2 == '':
                label2txt=''
            else:
                label2txt=codetranslate(ticker2)+"("+trend_txt+")"            
            plt.plot(df2.index, f(df2.id),"r--", label=label2txt,linewidth=1)
        except: pass
    
    # 同轴绘图时，loc1/loc2未用上！
    plt.legend(loc=loc1,fontsize=legend_txt_size)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.ylabel(ylabeltxt,fontsize=ylabel_txt_size)
    plt.xlabel(footnote,fontsize=xlabel_txt_size)
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    plt.show()
    plt.close()
    
    return

#==============================================================================
def plot_line2_twinx(df01,ticker1,colname1,label1, \
                     df02,ticker2,colname2,label2, \
                    titletxt,footnote,power=0,datatag1=False,datatag2=False, \
                    resample_freq='H',loc1='upper left',loc2='lower left', \
                    color1='red',color2='blue'):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制双轴折线图
    返回值：无
    注意：需要日期类型作为df索引
    """
    plt.rcParams['axes.grid']=False
    
    #插值平滑
    try:
        df01x=df01[[colname1]].astype('float')
        df1=df_smooth_manual(df01x,resample_freq=resample_freq)
    except:
        df1=df01
    try:
        df02x=df02[[colname2]].astype('float')
        df2=df_smooth_manual(df02x,resample_freq=resample_freq)
    except:
        df2=df02
        
    #证券1：绘制折线图，双坐标轴
    import matplotlib.dates as mdates
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    if ticker1 == '':
        label1txt=label1
    else:
        if label1 == '':
            label1txt=codetranslate(ticker1)
        else:
            label1txt=codetranslate(ticker1)+'('+label1+')'    
    
    ax.plot(df1.index,df1[colname1],'-',label=label1txt, \
             linestyle='-',color=color1,linewidth=2)   
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            ax.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')

    #绘证券1：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'        
        
        #生成行号，借此将横轴的日期数量化，以便拟合
        df1['id']=range(len(df1))
        
        #设定多项式拟合，power为多项式次数
        import numpy as np
        parameter = np.polyfit(df1.id, df1[colname1], power)
        f = np.poly1d(parameter)

        if ticker1 == '':
            label1txt=''
        else:
            label1txt=codetranslate(ticker1)+"("+trend_txt+")"
        ax.plot(df1.index, f(df1.id),"r--", label=label1txt,linewidth=1)

    #绘证券2：建立第二y轴
    ax2 = ax.twinx()
    
    if ticker2 == '':
        label2txt=label2
    else:
        if label2 == '':
            label2txt=codetranslate(ticker2)
        else:
            label2txt=codetranslate(ticker2)+'('+label2+')'    
    
    ax2.plot(df2.index,df2[colname2],'-',label=label2txt, \
             linestyle='-.',color=color2,linewidth=2.5)
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            ax2.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')
    
    #绘证券2：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'           
        
        #生成行号，借此将横轴的日期数量化，以便拟合
        df2['id']=range(len(df2))
        
        #设定多项式拟合，power为多项式次数
        import numpy as np
        parameter = np.polyfit(df2.id, df2[colname2], power)
        f = np.poly1d(parameter)

        if ticker2 == '':
            label2txt=''
        else:
            label2txt=codetranslate(ticker2)+"("+trend_txt+")"
        ax2.plot(df2.index, f(df2.id),"c--", label=label2txt,linewidth=1)        
        
    ax.set_xlabel(footnote,fontsize=xlabel_txt_size)
    
    if ticker1 == '':
        label1txt=label1
    else:
        if label1 == "":
            label1txt=codetranslate(ticker1)
        else:
            label1txt=label1+'('+codetranslate(ticker1)+')'
    ax.set_ylabel(label1txt,fontsize=ylabel_txt_size)
    ax.legend(loc=loc1,fontsize=legend_txt_size)
    
    if ticker2 == '':
        label2txt=label2
    else:
        if label2 == "":
            label2txt=codetranslate(ticker2)
        else:
            label2txt=label2+'('+codetranslate(ticker2)+')'
    ax2.set_ylabel(label2txt,fontsize=ylabel_txt_size)
    ax2.legend(loc=loc2,fontsize=legend_txt_size)
    
    #自动优化x轴标签
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    plt.show()
    
    return


if __name__ =="__main__":
    df1 = get_price('000002.SZ', '2020-1-1', '2020-3-16')
    df2 = get_price('600266.SS', '2020-1-1', '2020-3-16')
    ticker1='000002.SZ'; ticker2='600266.SS'
    colname1='Close'; colname2='Close'
    label1="收盘价"; label2="收盘价"
    ylabeltxt="价格"
    plot_line2_twinx(df1,'000002.SZ','Close','收盘价', \
        df2,'600266.SS','Close','收盘价', \
        "证券价格走势对比图","数据来源：新浪/stooq")

    plot_line2_twinx(df1,'000002.SZ','Close','收盘价', \
        df2,'600266.SS','Close','收盘价', \
        "证券价格走势对比图","数据来源：新浪/stooq",power=3)

#==============================================================================
def plot_line2_twinx2(df01,ticker1,colname1,label1, \
                     df02,ticker2,colname2,label2, \
                     titletxt,footnote,power=0,datatag1=False,datatag2=False, \
                     resample_freq='H',loc1='upper left',loc2='lower left', \
                     date_range=False,date_freq=False,date_fmt='%Y-%m-%d', \
                     color1='red',color2='blue'):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制双轴折线图
    返回值：无
    注意：需要日期类型作为df索引
    """
    plt.rcParams['axes.grid']=False

    #插值平滑
    try:
        df01x=df01[[colname1]].astype('float')
        df1=df_smooth_manual(df01x,resample_freq=resample_freq)
    except:
        df1=df01
    try:
        df02x=df02[[colname2]].astype('float')
        df2=df_smooth_manual(df02x,resample_freq=resample_freq)
    except:
        df2=df02
        
    #证券1：绘制折线图，双坐标轴
    import matplotlib.dates as mdate
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    if ticker1 == '':
        label1txt=label1
    else:
        if label1 == '':
            label1txt=codetranslate(ticker1)
        else:
            label1txt=codetranslate(ticker1)+'('+label1+')'    
        
    date_start=df1.index[0]
    date_end=df1.index[-1]
    if date_range and not date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))    
        
    ax.plot(df1.index,df1[colname1],'-',label=label1txt, \
             linestyle='-',color=color1,linewidth=2)   
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            ax.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')

    #绘证券1：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'           
        
        #生成行号，借此将横轴的日期数量化，以便拟合
        df1['id']=range(len(df1))
        
        #设定多项式拟合，power为多项式次数
        import numpy as np
        parameter = np.polyfit(df1.id, df1[colname1], power)
        f = np.poly1d(parameter)

        if ticker1 == '':
            label1txt=''
        else:
            label1txt=codetranslate(ticker1)+"("+trend_txt+")"
        ax.plot(df1.index, f(df1.id),"r--", label=label1txt,linewidth=1)

    #绘证券2：建立第二y轴
    ax2 = ax.twinx()
    
    if ticker2 == '':
        label2txt=label2
    else:
        if label2 == '':
            label2txt=codetranslate(ticker2)
        else:
            label2txt=codetranslate(ticker2)+'('+label2+')'    
        
    date_start=df2.index[0]
    date_end=df2.index[-1]
    if date_range and not date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))        
        
    ax2.plot(df2.index,df2[colname2],'-',label=label2txt, \
             linestyle='-.',color=color2,linewidth=2.5)
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            ax2.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')
    
    #绘证券2：制趋势线
    if power > 0:
        lang=check_language()
        trend_txt='趋势线'
        if lang == 'English':
            trend_txt='Trend line'           
        
        #生成行号，借此将横轴的日期数量化，以便拟合
        df2['id']=range(len(df2))
        
        #设定多项式拟合，power为多项式次数
        import numpy as np
        parameter = np.polyfit(df2.id, df2[colname2], power)
        f = np.poly1d(parameter)

        if ticker2 == '':
            label2txt=''
        else:
            label2txt=codetranslate(ticker2)+"("+trend_txt+")"
        ax2.plot(df2.index, f(df2.id),"c--", label=label2txt,linewidth=1)        
        
    ax.set_xlabel(footnote,fontsize=xlabel_txt_size)
    
    if ticker1 == '':
        label1txt=label1
    else:
        if label1 == "":
            label1txt=codetranslate(ticker1)
        else:
            label1txt=label1+'('+codetranslate(ticker1)+')'
    ax.set_ylabel(label1txt,fontsize=ylabel_txt_size)
    ax.legend(loc=loc1,fontsize=legend_txt_size)
    
    if ticker2 == '':
        label2txt=label2
    else:
        if label2 == "":
            label2txt=codetranslate(ticker2)
        else:
            label2txt=label2+'('+codetranslate(ticker2)+')'
    ax2.set_ylabel(label2txt,fontsize=ylabel_txt_size)
    ax2.legend(loc=loc2,fontsize=legend_txt_size)
    
    #自动优化x轴标签
    #格式化时间轴标注
    #plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%y-%m-%d')) 
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    plt.show()
    
    return

#==============================================================================
def draw_lines(df0,y_label,x_label,axhline_value,axhline_label,title_txt, \
               data_label=True,resample_freq='H',smooth=True,linewidth=1.5, \
               loc='best',annotate=False,annotate_value=False):
    """
    函数功能：根据df的内容绘制折线图
    输入参数：
    df：数据框。有几个字段就绘制几条折现。必须索引，索引值将作为X轴标记点
    要求：df的索引为pandas的datetime日期型
    axhline_label: 水平辅助线标记。如果为空值则不绘制水平辅助线
    axhline_value: 水平辅助线的y轴位置
    y_label：y轴标记
    x_label：x轴标记
    title_txt：标题。如需多行，中间用\n分割
    
    输出：
    绘制折线图
    无返回数据
    注意：需要日期类型作为df索引
    """
    #空值判断
    if len(df0) ==0:
        print ("  #Warning(draw_lines): no data to plot.")
        return
    
    #插值平滑
    if smooth:
        print("  Rendering graphics ...")
        try:
            df=df_smooth_manual(df0,resample_freq=resample_freq)
        except:
            df=df0
    else:
        df=df0
        
    #取得df字段名列表
    collist=df.columns.values.tolist()  
    if len(collist) > 16:
        print ("  #Warning(draw_lines): too many columns to draw lines, max 16 lines")
        return
    
    lslist=['-','--','-.',':','-','--','-.',':','-','--','-.',':','-','--','-.',':',]
    #mklist=[',','d','_','.','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D']
    mklist=[',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',']
    
    # 所有字段转换为数值类型，以防万一
    for c in collist:
        df[c]=df[c].astype('float')
    
    """
    # 计算所有列中的最大最小差距
    dfmax=0; dfmin=0
    for c in collist:
        cmax=df[c].max()
        if cmax > dfmax:
            dfmax=cmax
        
        cmin=df[c].min()
        if cmin < dfmin:
            dfmin=cmin
    dfspread=(dfmax - dfmin)/10.0
    """
    
    # 将末端值最大的排在第一列，优先绘图
    dftt=df.T
    lastrow=list(dftt)[-1]
    dftt.sort_values(lastrow,ascending=False,inplace=True)
    df2=dftt.T
    
    # 最上层线标志
    firstline=True
    
    #绘制折线图
    y_end_list=[]    
    for c in collist:
        pos=collist.index(c)
        try:
            lsc=lslist[pos]
        except:
            print("  #Bug(draw_lines): lslist=",lslist,",pos=",pos)
        mkc=mklist[pos]
        
        # 连接折线中非交易日的断开区间
        import pandas as pd
        dfg=pd.DataFrame(df2[c]).copy(deep=True)
        
        # 慎用dropna
        #dfg=dfg.dropna(inplace=True)
        if dfg is None:
            print("  #Error(draw_lines): null dataframe for graphics in column",c)
            continue
        if len(dfg)==0:
            print("  #Error(draw_lines): no data for graphics in column",c)
            continue
        
        #plt.plot(dfg,label=c,linewidth=linewidth,ls=lsc,marker=mkc,markersize=3)
        if not annotate:
            """
            注意：许多传入的df字段名已经不是证券代码，此处调用codetranslate将会导致
            股票名称字典重新下载，耗费时间，且出现黄条。
            建议：在调用draw_lines之前，先调用codetranslate，将证券代码翻译为证券名称。
            本函数仅负责绘图，不负责翻译证券名称。
            """
            #plt.plot(dfg,label=codetranslate(c),linewidth=linewidth,ls=lsc,marker=mkc,markersize=3)
            plt.plot(dfg,label=c,linewidth=linewidth,ls=lsc,marker=mkc,markersize=3)
        else:
            #plt.plot(dfg[c],label=codetranslate(c),linewidth=linewidth,ls=lsc,marker=mkc,markersize=3)
            #plt.plot(dfg,label=codetranslate(c),linewidth=linewidth,ls=lsc,marker=mkc,markersize=3)
            plt.plot(dfg,label=c,linewidth=linewidth,ls=lsc,marker=mkc,markersize=3)
            
            df_end=dfg.tail(1)
            # df_end[c]必须为数值类型，否则可能出错
            y_end = df_end[c].min()    # 末端的y坐标
            x_end = df_end[c].idxmin() # 末端值的x坐标 
            
            """
            if firstline:
                # 直接绘图
                firstline=False
                y_prev=y_end
            else:
                distance=y_prev - y_end
                if distance < dfspread:
                    y_end=y_end - dfspread
                    y_prev=y_end
            y_end_list=y_end_list+[y_end]
            """
            """
            plt.annotate(text=codetranslate(c)+':'+str(round(y_end,2)), 
                                 xy=(x_end, y_end),
                                 xytext=(x_end, y_end),fontsize=9)   
            """
            if annotate_value:
                plt.annotate(text=c+':'+str(round(y_end,2)), 
                                 xy=(x_end, y_end),
                                 xytext=(x_end, y_end),fontsize=9)
            else:
                plt.annotate(text=c, 
                                 xy=(x_end, y_end),
                                 xytext=(x_end, y_end),fontsize=9)
                
        #plt.plot(df[c],label=c,linewidth=1.5,marker=mkc,markersize=3)
        #为折线加数据标签
        if data_label==True:
            for a,b in zip(df2.index,df2[c]):
                plt.text(a,b+0.02,str(round(b,2)), \
                         ha='center',va='bottom',fontsize=7)
    
    #绘制水平辅助线
    if axhline_label !="":
        if '零线' in axhline_label:
            axhline_label=''
        plt.axhline(y=axhline_value,label=axhline_label,color='black',linestyle=':',linewidth=2)  
        #plt.axhline(y=axhline_value,color='purple',linestyle=':',linewidth=1.5)
    
    #坐标轴标记
    y_label_t=ectranslate(y_label)
    plt.ylabel(y_label_t,fontweight='bold',fontsize=ylabel_txt_size)
    
    x_label_t=ectranslate(x_label)
    if x_label != "":
        plt.xlabel(x_label_t,fontweight='bold',fontsize=xlabel_txt_size)
    #图示标题
    plt.title(title_txt,fontweight='bold',fontsize=title_txt_size)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    # 若绘制annotate，则可不绘制图例
    if not annotate:
        plt.legend(loc=loc,fontsize=legend_txt_size)
    
    plt.show()
    
    return    
    
if __name__=='__main__':
    title_txt="Stock Risk \nCAPM Beta Trends"
    draw_lines(df,"market line",1.0,"Beta coefficient","",title_txt)    

#==============================================================================
def draw_lines2(df0,y_label,x_label,axhline_value,axhline_label,title_txt, \
               data_label=False,resample_freq='6H',smooth=True, \
               date_range=False,date_freq=False,date_fmt='%Y-%m-%d', \
               colorlist=[],lslist=[],lwlist=[]):
    """
    函数功能：根据df的内容绘制折线图
    输入参数：
    df：数据框。有几个字段就绘制几条折现。必须索引，索引值将作为X轴标记点
    要求：df的索引为pandas的datetime日期型
    axhline_label: 水平辅助线标记。如果为空值则不绘制水平辅助线
    axhline_value: 水平辅助线的y轴位置
    y_label：y轴标记
    x_label：x轴标记
    title_txt：标题。如需多行，中间用\n分割
    
    smooth=True：默认进行曲线平滑处理，对于部分长期停牌的股票/债券，应选择不进行平滑处理False，否则曲线会严重失真。
    
    输出：
    绘制折线图
    无返回数据
    注意：需要日期类型作为df索引
    """
    #空值判断
    if len(df0) ==0:
        print ("  #Warning(draw_lines): no data to plot.")
        return
    
    #插值平滑
    if smooth:
        print("  Smoothening curves ...")
        try:
            df=df_smooth_manual(df0,resample_freq=resample_freq)
        except:
            df=df0
    else:
        df=df0

    #定义横轴标签：显示完整开始、结束日期
    import matplotlib.dates as mdate
    ax=plt.gca()    
    date_start=df.index[0]
    date_end=df.index[-1]
    if date_range and not date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))    
        
    #取得df字段名列表
    collist=df.columns.values.tolist()  
    
    #绘制折线图    
    for c in collist:
        pos=collist.index(c)
        try:
            lcolor=colorlist[pos]
            lls=lslist[pos]
            llw=lwlist[pos]
        except:
            plt.plot(df[c],label=c,linewidth=2)
        else:
            plt.plot(df[c],label=c,linewidth=llw,ls=lls,color=lcolor)
        
        #为折线加数据标签
        if data_label==True:
            for a,b in zip(df.index,df[c]):
                plt.text(a,b+0.02,str(round(b,2)), \
                         ha='center',va='bottom',fontsize=7)
    
    #绘制水平辅助线
    if axhline_label !="":
        if "零线" in axhline_label:
            plt.axhline(y=axhline_value,color='black',linestyle='--',linewidth=2)  
        else:
            plt.axhline(y=axhline_value,label=axhline_label,color='black',linestyle='--',linewidth=2)  
    
    #坐标轴标记
    plt.ylabel(y_label,fontweight='bold',fontsize=ylabel_txt_size)
    if x_label != "":
        plt.xlabel(x_label,fontweight='bold',fontsize=xlabel_txt_size)
    #图示标题
    plt.title(title_txt,fontweight='bold',fontsize=title_txt_size)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.legend(loc='best',fontsize=legend_txt_size)
    plt.show()
    
    return    

#==============================================================================
def plot_barh(df,colname,titletxt,footnote,datatag=True, \
              colors=['r','g','b','c','m','y','aquamarine','dodgerblue', \
              'deepskyblue','silver'],tag_offset=0.01,axisamp=1.3):
    """
    功能：绘制水平单值柱状图，并可标注数据标签。
    输入：数据集df；列名colname；标题titletxt；脚注footnote；
    是否绘制数据标签datatag，默认是；柱状图柱子色彩列表。
    输出：水平柱状图
    """
    #空值判断
    if len(df) ==0:
        print ("  #Warning(plot_barh): no data to plot.")
        return

    plt.barh(df.index,df[colname],align='center',color=colors,alpha=0.8)
    coltxt=ectranslate(colname)
    plt.xlabel(footnote,fontsize=xlabel_txt_size)
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    
    #xmin=int(min(df[colname]))
    xmin0=min(df[colname])
    if xmin0 > 0:
        xmin=xmin0*0.8
    else:
        xmin=xmin0*1.05
    #xmax=(int(max(df[colname]))+1)*1.1
    xmax0=max(df[colname])
    if not (xmax0 == 0):
        scale_max=abs((xmax0-xmin0)/xmax0)*axisamp  #经验值放大倍数
        xmax=xmax0*scale_max
    else:
        scale_max=abs((xmax0-xmin0))*axisamp
        xmax=xmax0+scale_max
    
    """
    if xmax0 > 0:
        xmax=xmax0*1.8
    else:
        xmax=xmax0*1.2
    """
    plt.xlim([xmin,xmax])
    
    tag_off=tag_offset * xmax
    for x,y in enumerate(list(df[colname])):
        #plt.text(y+0.1,x,'%s' % y,va='center')
        plt.text(y+tag_off,x,'%s' % y,va='center')

    """
    yticklist=list(df.index)
    yticknames=[]
    for yt in yticklist:
        ytname=codetranslate(yt)
        yticknames=yticknames+[ytname]
    """
    yticknames=list(df.index)
    plt.yticks(df.index,yticknames)

    plt.show(); plt.close()
    
    return

#==============================================================================
if __name__=='__main__':
    import pandas as pd
    df = pd.read_excel('S:/QTEMP/px_test.xlsx',header=0, index_col=0)  
    
    colname='Exp Ret%'
    titletxt="This is a title"
    footnote="This is a footnote"

def plot_barh2(df,colname,titletxt,footnote):
    """
    功能：绘制水平单值柱状图，并在外侧标注数据标签。
    输入：数据集df；列名colname；标题titletxt；脚注footnote；
    输出：水平柱状图
    注意：在Spyder中可能工作不正常，使用plotly_express.bar
    """
    #空值判断
    if len(df) ==0:
        print ("  #Warning(plot_barh): no data to plot.")
        return

    #改造df
    df['ycolname']=df.index
    df['xcolname']=df[colname]
    xlabel=colname+'颜色棒'
    df[xlabel]=df[colname]

    import plotly_express as px
    
    fig=px.bar(data_frame = df, 
               y='ycolname', #纵轴绘制的字段
               x=colname, #横轴绘制的字段
               color=xlabel, #基于df中xlabel字段的数值大小配色，并将xlabel作为颜色棒顶部的标注
               orientation='h', #绘制水平直方图
               text=colname, #在直方图顶端标数字
               labels={'ycolname':'',colname:footnote,xlabel:''} #将字段改名作为纵轴、横轴或颜色棒的标注
        )
    
    fig.update_traces(textposition='outside') #直方图顶端的数值标在外侧
    
    fig.update_layout(
        title={
            'text': titletxt,   # 标题名称
            'y':0.95,  # 位置，坐标轴的长度看做1
            'x':0.5,
            'xanchor': 'center',   # 相对位置
            'yanchor': 'top'},
        )

    fig.show()
    
    return

if __name__=='__main__':
    plot_barh2(df,colname,titletxt,footnote)
#==============================================================================

#==============================================================================
#==============================================================================
def plot_2lines(df01,colname1,label1, \
                df02,colname2,label2, \
                ylabeltxt,titletxt,footnote,hline=0,vline=0,resample_freq='H', \
                date_range=False,date_freq=False,date_fmt='%Y-%m-%d'):
    """
    功能：绘制两个证券的折线图。如果hline=0不绘制水平虚线，vline=0不绘制垂直虚线
    假定：数据表有日期索引，且已经按照索引排序
    输入：
    证券1：数据表df1，列名1，列名标签1；
    证券2：数据表df2，列名2，列名标签2；
    标题titletxt，脚注footnote
    输出：绘制同轴折线图
    
    若date_range=True，尽量在横轴上标注日期的起止时间
    若date_freq不为False，可以为类似于'3m'或'1Y'等
    date_fmt可以为'%Y-%m-%d'或'%Y-%m'或'%Y'等
    
    返回值：无
    """
    #空值判断
    if len(df01) ==0:
        print ("  #Warning(plot_2lines): no data to plot df01.")
    if len(df02) ==0:
        print ("  #Warning(plot_2lines): no data to plot df02.")   
    if (len(df01) ==0) and (len(df02) ==0):
        return

    #插值平滑
    try:
        df01x=df01[[colname1]].astype('float')
        df1=df_smooth_manual(df01x,resample_freq=resample_freq)
    except:
        df1=df01
        
    try:
        df02x=df02[[colname2]].astype('float')        
        df2=df_smooth_manual(df02x,resample_freq=resample_freq)
    except:
        df2=df02
    
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    
    #证券1：先绘制折线图
    import matplotlib.dates as mdate
    date_start=df1.index[0]
    date_end=df1.index[-1]
    if date_range and not date_freq:
        ax=plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax=plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax=plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))
    
    plt.plot(df1.index,df1[colname1],label=label1,linestyle='-',linewidth=2)
    
    #证券2：先绘制折线图
    date_start=df2.index[0]
    date_end=df2.index[-1]
    if date_range and not date_freq:
        ax=plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end))
    if not date_range and date_freq:
        ax=plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(freq=date_freq))
    if date_range and date_freq:
        ax=plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter(date_fmt))
        plt.xticks(pd.date_range(date_start,date_end,freq=date_freq))
        
    plt.plot(df2.index,df2[colname2],label=label2,linestyle='-.',linewidth=2.5)
    
    #是否绘制水平虚线
    if not (hline == 0):
        plt.axhline(y=hline,ls=":",c="black")
    #是否绘制垂直虚线
    if not (vline == 0):
        plt.axvline(x=vline,ls=":",c="black")
    
    plt.ylabel(ylabeltxt,fontsize=ylabel_txt_size)
    plt.xlabel(footnote,fontsize=xlabel_txt_size)
    plt.legend(loc='best',fontsize=legend_txt_size)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.show()
    
    return

if __name__ =="__main__":
    df1=bsm_call_maturity(42,40,[50,200],0.015,0.23,90,1.5)
    df2=bsm_put_maturity(42,40,[50,200],0.015,0.23,90,1.5)
    ticker1='A'; colname1='Option Price'; label1='A1'
    ticker2='B'; colname2='Option Price'; label2='B2'
    ylabeltxt='ylabel'; titletxt='title'; footnote='\n\n\n\n4lines'
    power=0; datatag1=False; datatag2=False; zeroline=False
    
#==============================================================================
def df_smooth(df):
    """
    功能：对df中的数值型样本进行插值，以便绘制的折线图相对平滑。
    要求：df的索引为pandas的datetime日期型
    注意1：如果样本数量较多，例如多于100个，平滑效果不明显。
    注意2：order阶数仅对'spline'和'polynomial'方法有效，其中'polynomial'方法的阶数只能为奇数。
    """
    
    #如果样本个数多于100个，其实没必要进行平滑，因为看不出效果
    if len(df) >= 100: return df
    
    #定义重采样频率
    """
    常用的采样频率：
    H: hourly, BH: business hour, T: minutely, S: secondly, B: business day, W: weekly, 
    SM: semi-month end, SMS: semi-month start, 
    BMS: business month start,BM: business month end,
    BQ: business quarter end, BQS: business quarter start,
    BA/BY: business year end, BAS/BYS: business year start.    
    
    例如：
    df2=df.resample('2D').sum()
    df2=df.resample('W').mean()
    """
    #将索引转换为Datetimeindex，不然resample会失败
    df['date']=pd.to_datetime(df.index)
    df.set_index('date',inplace=True)
    
    #重新采样
    rflag=False
    freqlist=['H','B','W','M','Q']
    for f in freqlist:
        try:
            #dfh=df.resample(f).ffill()
            dfh=df.resample(f)
        except:
            continue
        else:
            rflag=True
            break
    
    if not rflag: 
        #print('  #Warning(df_smooth): resampling failed for frequency',freqlist)
        dfh=df
    
    #插值
    methodlist=['pchip','nearest','cubic','quadratic','slinear','linear','zero','time','index', \
            'piecewise_polynomial','akima','from_derivatives','spline','polynomial']
    methodlist_order=['spline','polynomial']
    order=3
    for method in methodlist:
        if method in methodlist_order:
            try:
                dfm=dfh.interpolate(method=method,order=order)
            except:
                #print('  #Warning(df_smooth): interpolate failed for method',method,'with order',order)
                #若出错就原样返回
                return df
            else: break
        else:
            try:
                dfm=dfh.interpolate(method=method)
            except:
                #print('  #Warning(df_smooth): interpolate failed for method',method)
                return df
            else: break
    
    #成功返回经过重采样的df
    return dfm        
    
        
#==============================================================================
def df_smooth_manual(df,method='pchip',resample_freq='H',order=3):
    """
    功能：对df中的第一个数值列样本进行插值，以便绘制的折线图相对平滑。
    要求：df的索引为pandas的datetime日期型
    注意1：如果样本数量较多，例如多于100个，平滑效果不明显。
    注意2：order阶数仅对'spline'和'polynomial'方法有效，其中'polynomial'方法的阶数只能为奇数。
    注意3：pchip方法经常失败，改为cubic
    """
    
    #如果样本个数多于100个，没必要进行平滑，完全看不出效果
    if len(df) >= 100: return df
    
    #检查平滑方法是否支持
    methodlist=['quadratic','cubic','slinear','linear','zero','nearest','time','index', \
            'piecewise_polynomial','pchip','akima','from_derivatives','spline','polynomial']
    if not (method in methodlist): return df
    
    #定义重采样频率
    """
    常用的采样频率：
    H: hourly, BH: business hour, T: minutely, S: secondly, B: business day, W: weekly, 
    SM: semi-month end, SMS: semi-month start, 
    BMS: business month start,BM: business month end,
    BQ: business quarter end, BQS: business quarter start,
    BA/BY: business year end, BAS/BYS: business year start.    
    
    例如：
    df2=df.resample('2D').sum()
    df2=df.resample('W').mean()
    """
    #将索引转换为Datetimeindex，不然resample会失败
    try:
        df['date']=pd.to_datetime(df.index)
    except:
        return df
    df.set_index('date',inplace=True)    
    
    try:
        dfh=df.resample(resample_freq)
    except:
        print('  #Warning(df_smooth): resampling failed for frequency',resample_freq)
        return df
    
    #重新采样
    methodlist_o=['spline','polynomial']
    if method in methodlist_o:
        try:
            dfm=dfh.interpolate(method=method,order=order)
        except:
            print('  #Warning(df_smooth_manual): interpolate failed for method',method,'with order',order)
            #若出错就原样返回
            return df
        #成功返回经过重采样的df
        return dfm
    
    try:
        dfm=dfh.interpolate(method=method)
    except:
        #print('  #Warning(df_smooth_manual): interpolate failed for method',method)
        #print('  Possible reason: interpolating row must be int or float instead of string')
        """
        #改为cubic方法
        if not (method == 'cubic'):
            try:
                dfm=dfh.interpolate(method='cubic')
            except:
                print('  #Warning(df_smooth_manual): interpolate failed for method cubic')    
                return df
        else:
            return df
        """
        return df
    
    # check whether dfm becomes empty
    if len(dfm)==0:
        return df
    else:
        return dfm        
#==============================================================================
if __name__=='__main__':
    wid=5
    mu=0
    sd=1
    obs_num=100
    
def plot_norm(mu,sd,graph='pdf',obs_num=100):
    """
    绘制正态分布图形
    mu:均值
    sd:标准差
    graph:图形种类,pdf,cdf,ppf
    """
    if not (graph in ['pdf','cdf','ppf']):
        print("  #Warning(plot_norm): support pdf/cdf/ppf only")
        return
    
    #计算概率密度:连续分布用pdf,离散分布用pmf
    import scipy.stats as st
    import numpy as np
    
    if graph=='pdf':
        wid=4*sd+mu
        X=np.linspace(-wid,wid,obs_num)
        y_pdf=st.norm.pdf(X,mu,sd) 
    
    if graph=='cdf':
        wid=3*sd+mu
        X=np.linspace(-wid,wid,obs_num)        
        y_cdf=st.norm.cdf(X,mu,sd)
        
    if graph=='ppf':
        X=np.linspace(0,1,obs_num)
        y_ppf=st.norm.ppf(X,mu,sd)

    #绘图
    if graph=='pdf':
        plt.plot(X,y_pdf,c="red",label='pdf')
    if graph=='cdf':
        plt.plot(X,y_cdf,c="blue",label='cdf')
    if graph=='ppf':
        plt.plot(X,y_ppf,c="green",label='ppf')
    
    if graph=='pdf':
        wid1=5*sd+mu
        wid2=1*sd+mu
        plt.xticks(np.arange(-wid,wid1,wid2))
        plt.xlabel('分位点',fontsize=xlabel_txt_size) #x轴文本
        plt.yticks(np.arange(0,0.45,0.05))
        plt.ylabel('概率密度',fontsize=ylabel_txt_size) #y轴文本

    if graph=='cdf':
        wid1=3.5*sd+mu
        wid2=0.5*sd+mu        
        plt.xticks(np.arange(-wid,wid1,wid2))
        plt.xlabel('分位点',fontsize=xlabel_txt_size) #x轴文本
        plt.yticks(np.arange(0,1.1,0.1))
        plt.ylabel('累积概率密度',fontsize=ylabel_txt_size) #y轴文本

    if graph=='ppf':
        wid=2.5*sd+mu
        wid1=3*sd+mu
        wid2=0.5*sd+mu
        plt.yticks(np.arange(-wid,wid1,wid2))
        plt.ylabel('分位点',fontsize=ylabel_txt_size) #y轴文本
        plt.xticks(np.arange(0,1.1,0.1))
        plt.xlabel('累积概率密度',fontsize=xlabel_txt_size) #x轴文本        
        
    plt.title('正态分布示意图: $\mu$=%.1f, $\sigma$=%.1f'%(mu,sd),fontweight='bold',fontsize=title_txt_size) #标题
    plt.tight_layout()
    plt.grid() #网格
    plt.legend(loc='best',fontsize=legend_txt_size)
    plt.show() #显示图形
    
    return

if __name__=='__main__':
    plot_norm(4,mu,sd,graph='pdf')
    plot_norm(3,mu,sd,graph='cdf')
    plot_norm(3,mu,sd,graph='ppf')        
    
#==============================================================================    
#==============================================================================

if __name__=='__main__':
    firstColSpecial=True
    colWidth=0.1
    tabScale=2
    figsize=(10,6)
    cellLoc='right'
    fontsize=10

    firstColSpecial=False
    cellLoc='center'
    auto_len=True
    
    df=market_detail_china(category='price')
    pandas2plttable(df)

def pandas2plttable(df,titletxt,firstColSpecial=True,colWidth=0.1,tabScale=2,cellLoc='right', \
                    figsize=(10,4),fontsize=13,auto_len=False,title_x=0.5):
    """
    功能：将一个df转换为matplotlib表格格式，打印图形表格，适应性广
    firstColSpecial：第一列是否特殊处理，默认True
    
    注意1：引入表格的字段不包括索引字段
    """  
    
    #列名列表
    col=list(df)
    numOfCol=len(col)
    
    # 第一列长度取齐处理
    if firstColSpecial:
        #第一列的最长长度
        firstcol=col[0]
        maxlen=0
        for f in firstcol:
            flen=hzlen(f.strip())
            if flen > maxlen:
                maxlen=flen
        
        #将第一列内容的长度取齐
        df[col[0]]=df[col[0]].apply(lambda x:equalwidth(x.strip(),maxlen=maxlen,extchar=' ',endchar=' '))    
    
    #设置每列的宽度
    col_len_list=[]
    col_len_list_rel=[]
    if auto_len:
        
        # 计算每列的相对宽度
        for c in col:
            heading_len=hzlen(c.strip())
            df['col_len']=df[c].apply(lambda x: hzlen(x.strip()))
            field_len=df['col_len'].max()
            col_len=max([heading_len,field_len])
            
            col_len_list=col_len_list+[col_len]

        col_len_min=min(col_len_list)
        for l in col_len_list:
            rel_len=l / col_len_min               
            col_len_list_rel=col_len_list_rel+[round(rel_len*colWidth,3)]
            
        del df['col_len']
    
    
    #表格里面的具体值
    vals=[]
    for i in range(0,len(df)): 
        vals=vals+[list(df.iloc[i])]
    
    #plt.figure(figsize=figsize,dpi=figdpi)
    plt.figure(figsize=figsize)
    
    if not auto_len:
        tab = plt.table(cellText=vals, 
                      colLabels=col, 
                      loc='best', 
                      cellLoc=cellLoc)
    else:
        tab = plt.table(cellText=vals, 
                      colLabels=col, 
                      colWidths=col_len_list_rel,
                      loc='best', 
                      rowLoc='center',
                      cellLoc=cellLoc)
            
    
    tab.scale(1,tabScale)   #让表格纵向扩展tabScale倍数
    
    # 试验参数：查询tab对象的属性使用dir(tab)
    tab.auto_set_font_size(False)
    tab.set_fontsize(fontsize)
    
    if auto_len:
        tab.auto_set_column_width(True)    #此功能有bug，只能对前几列起作用
    
    plt.axis('off')         #关闭plt绘制纵横轴线
    
    #plt.xlabel(footnote,fontsize=xlabel_txt_size)
    if not auto_len:
        plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    else:
        plt.title(titletxt,fontweight='bold',fontsize=title_txt_size,x=title_x)
    
    plt.show()

    return

#==============================================================================

if __name__=='__main__':
    firstColSpecial=True
    colWidth=0.1
    tabScale=2
    figsize=(10,6)
    cellLoc='right'
    fontsize=10

    firstColSpecial=False
    cellLoc='center'
    auto_len=True
    
    df=market_detail_china(category='price')
    pandas2plttable(df)

def pandas2plttable2(df,titletxt,firstColSpecial=True,cellLoc='right'):
    """
    功能：将一个df转换为matplotlib表格格式，打印图形表格，适应性广，自动适应列宽和字体大小
    firstColSpecial：第一列是否特殊处理，默认True
    
    注意1：引入表格的字段不包括索引字段
    """  
    
    df.fillna('',inplace=True)
    
    #列名列表
    col=list(df)
    numOfCol=len(col)
    
    # 第一列长度取齐处理
    if firstColSpecial:
        
        #第一列的最长长度
        firstcol=col[0]
        maxlen=0
        for f in df[firstcol]:
            flen=hzlen(f)
            if flen > maxlen:
                maxlen=flen
        
        #将第一列内容的长度取齐
        extchar='.'
        df[firstcol]=df[firstcol].apply(lambda x: str(x) + extchar*(maxlen-hzlen(x)))    
    
    
    #表格里面的具体值
    vals=[]
    for i in range(0,len(df)): 
        vals=vals+[list(df.iloc[i])]
    
    plt.figure()
    
    tab = plt.table(cellText=vals, 
                  colLabels=col, 
                  loc='best', 
                  rowLoc='center',
                  cellLoc=cellLoc)
    
    #tab.scale(1,tabScale)   #让表格纵向扩展tabScale倍数
    
    # 试验参数：查询tab对象的属性使用dir(tab)
    tab.auto_set_font_size(True)
    
    tab.auto_set_column_width(True)    #此功能有bug，只能对前几列起作用
    
    plt.axis('off')         #关闭plt绘制纵横轴线
    
    plt.title(titletxt)
    
    plt.show()

    return


#==============================================================================    
#==============================================================================








