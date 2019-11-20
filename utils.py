import requests
import re
import time

"""存放打印需要的通用的方法"""
def getPrinterStatus(printerPort):
    printerHtml = ''
    try:
        printerHtml = requests.get('http://{0}/cgi-bin/status.cgi'.format(printerPort),timeout=0.25)
    except Exception as e:
        printerHtml = str(e)
    finally:
        regex = re.compile("greentext>.*?<")
        labelInfo = regex.findall(printerHtml)
        return labelInfo[0][10:-1] if len(labelInfo) >0  else  '网络不通'
"""获取目前时间"""
def getCurrentTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
