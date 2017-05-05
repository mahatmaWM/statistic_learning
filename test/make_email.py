# -*- coding: UTF8 -*-
import os
import datetime
import cx_Oracle
import re
import getopt, sys
import urllib2
import json
from xml.etree import ElementTree
import time
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from pylab import *
import string

reload(sys)
sys.setdefaultencoding('utf-8')


def GetDateString(day):
    time_today = time.localtime(time.time())
    date_today = datetime.datetime(time_today[0],time_today[1],time_today[2],time_today[3],time_today[4],time_today[5])
    date_return = date_today - datetime.timedelta(days = day)
    return str(date_return)[0:10]

def GetDateInt(day):
    time_today = time.localtime(time.time())
    date_today = datetime.datetime(time_today[0],time_today[1],time_today[2],time_today[3],time_today[4],time_today[5])
    date_return = date_today - datetime.timedelta(hours = day)
    return int(str(date_return)[0:13].replace('-','').replace(' ',''))


def call_url_xml(url):

    req = urllib2.Request(url,headers={'Accept':'application/xml'})
    f = urllib2.urlopen(req)
    data = f.read()
    return data

def print_log(msg):
    now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "["+now+"]:"+msg


db_mysql=MySQLdb.connect(host="adm01p.lufax.storage",port=3307,user="dbadmin",passwd="dbadmin",db="dbadmin",charset="utf8")
cursor_mysql=db_mysql.cursor()

def TupleToList(tuplevalue):
    listint = []
    for value in tuplevalue:
        if isinstance(value, tuple):
            value = value[0]
        listint.append(int(value))
    return listint

def do_report():
    yest_date = GetDateString(1).replace('-','')+"%"
    last7_date = GetDateString(8).replace('-','')+"%"
    last28_date = GetDateString(29).replace('-','')+"%"
    yest2_date = GetDateString(2).replace('-','')+"%"
    get_slow_query_sql="""
select t1.app_name,t1.domain,t1.owner,t1.dba,t1.namespace,t1.sqlmap_id,t1.count,t1.avg,t7.avg,t28.avg,o.db_unique_name
from 
(
 select a.app_name,b.domain,b.owner,ifnull(b.dba,'孙敏') as dba,namespace,sqlmap_id,count,round(avg/1000) as avg
 from cat_sql_info_daily a join app_info b 
 on a.app_name = b.app_name 
 where  a.app_name not in ('be-rrcl-srv','be-vrcl-srv') and namespace <> 'all' and snap_date like %s  order by avg desc limit 50
) t1
left join 
(
 select app_name,namespace,sqlmap_id,count,round(avg/1000) as avg
 from cat_sql_info_daily 
 where  namespace <> 'all' and snap_date like %s
) t7 on t1.app_name = t7.app_name and t1.namespace = t7.namespace and t1.sqlmap_id = t7.sqlmap_id 
left join 
(
 select app_name,namespace,sqlmap_id,count,round(avg/1000) as avg
 from cat_sql_info_daily 
 where  namespace <> 'all' and snap_date like %s
) t28 on t1.app_name = t28.app_name and t1.namespace = t28.namespace and t1.sqlmap_id = t28.sqlmap_id 
left join 
(
 select distinct app_name,namespace,sqlmap_id,db_unique_name from ora_sql_info_result where snap_date like %s
) o on t1.app_name = o.app_name and t1.namespace = o.namespace and t1.sqlmap_id = o.sqlmap_id
group by t1.app_name,t1.namespace,t1.sqlmap_id  
order by t1.avg desc;
"""
    n = cursor_mysql.execute(get_slow_query_sql,(yest_date,last7_date,last28_date,yest_date))
    app_list=list(cursor_mysql.fetchall())

    o = open(MAIL_BODY_FILE,'w')
    o.write("<html>\n")
    o.write("<b>昨日极慢SQL统计报告</b><br><br>")
    o.write("<table cellspacing=0 cellpadding=5 border=1 style=\"\"  bordercolor=\"\">\n")
    o.write("<tr bgcolor='#3B6588' style='color:White; font-weight:bold'>\n")
    o.write("<th>域名称</th><th>应用名称</th><th>域负责人</th><th>负责DBA</th><th>SQL模块名</th><th>昨日执行次数</th><th>昨日平均响应时间(秒)</th><th>7日前平均响应时间(秒)</th><th>28日前平均响应时间(秒)</th><th>DB实例</th>\n")
    o.write("</tr>\n")
    for app in app_list:
        app_name = app[0]
        domain = app[1]
        owner = app[2]
        dba = app[3]
        namespace = app[4]
        sqlmap_id = app[5]
        day_count = app[6]
        day_avg = app[7]
        l7day_avg = app[8]
        l28day_avg = app[9]
        dbname = app[10]

        o.write("<tr bgcolor='#EEEEEE'>\n")
        o.write("<td>"+domain+"</td><td>"+app_name+"</td><td>"+owner+"</td><td>"+dba+"</td><td>"+namespace+"."+sqlmap_id+"</td><td>"+str(day_count)+"</td><td>"+str(day_avg)+"</td><td>"+str(l7day_avg)+"</td><td>"+str(l28day_avg)+"</td><td>"+str(dbname)+"</td>\n")
        #o.write("<td>"+domain+"</td><td>"+app_name+"</td><td>"+owner+"</td><td>")
        o.write("</tr>\n")

    o.write("</table><br><br><br><br>\n")


MAIL_BODY_FILE = '/tmp/.slow_sqlreview_report.html'
TODAY_DATE = GetDateString(0)
MAIL_SENDER = 'abc@163.com'
MAIL_TITLE = '[AVA_RATE SQL Report][' + TODAY_DATE + ']'
#APPLIST=['be-rrcl-srv','be-vrcl-srv','user-app','fund-app','account-app','payment-app','accountr-app','tenpay-app','session-app','usersvc-app','trading-app','asset-app','p2p-app','lscheduler-app','yeb-app','jijin-app']
do_report()

os.system("perl /wls/dbadmin/tools/sendEmail -f lufax-cs@lufax.com -o message-charset=UTF-8 -s 30.33.224.15:25 -t %s -u '%s' -o message-file='%s' " % (MAIL_SENDER,MAIL_TITLE,MAIL_BODY_FILE))
