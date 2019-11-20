import pymssql
import configparser
import utils
"""与数据库交互"""
config = configparser.ConfigParser() #创建配置解析器对象
config.read('database.ini',encoding='gbk')  #读取并解析配置文件
printersdb = config['printersdb']  #返回printersdb节点信息
#获取数据库信息
databaseip = printersdb['databaseip']
databasename = printersdb['databasename']
username = printersdb['username']
password = printersdb['password']

"""获取打印机最新的全部信息"""
def getPrinterLatestData():
    list = []
    with pymssql.connect(databaseip, username, password, databasename) as conn:
        with conn.cursor(as_dict=True) as cursor:   #数据存放于字典中
            selectsql= 'select printercount,printername,portname,createtime,checkstatus  from printersinfo where createtime = (select max(createtime) from printersinfo )'
            cursor.execute(selectsql)
            for row in cursor:
                row['portstatus'] = utils.getPrinterStatus(row['portname']) if row['checkstatus'] == 'Y' else 'Disabled'
                row['checktime'] = utils.getCurrentTime()
                list.append(row)
    return list

"""通过打印端口修改打印机名称"""
def updatePrinterInfo(newPrinterName,oldPrinterName,portName):
    with pymssql.connect(databaseip, username, password, databasename) as conn:
        with conn.cursor() as cursor:
            updatesql =""
            if len(oldPrinterName) == 0:
                addPrinter(newPrinterName, portName)
            else:
                if newPrinterName == oldPrinterName:
                    updatesql = "update printersinfo set  portname='{0}' where printername='{1}' and createtime = (select max(createtime) from printersinfo )".format(portName, newPrinterName)
                else:
                    updatesql = "update printersinfo set  printername='{0}' where portname='{1}' and createtime = (select max(createtime) from printersinfo )".format(newPrinterName, portName)
            cursor.execute(updatesql)
            conn.commit()

"""通过打印端口查找打印机"""
def getOldPrinterName(portname,printername):
    with pymssql.connect(databaseip, username, password, databasename) as conn:
        with conn.cursor(as_dict=True) as cursor:
            selectsql = "select printername from printersinfo where (portname='{0}' or printername='{1}')  and createtime = (select max(createtime) from printersinfo)".format(portname,printername)
            cursor.execute(selectsql)
            row = cursor.fetchone()
            while row:
                return row['printername']
        return ""

"""删除指定打印机"""
def deletePrinterByPrinterName(printerName):
    with pymssql.connect(databaseip, username, password, databasename) as conn:
        with conn.cursor() as cursor:
            deletesql = "delete from printersinfo where printerName='{0}' and createtime = (select max(createtime) from printersinfo)".format(printerName)
            cursor.execute(deletesql)
            conn.commit()


"""增加打印机"""
def addPrinter(printerName,portName):
    with pymssql.connect(databaseip, username, password, databasename) as conn:
        with conn.cursor() as cursor:
            addsql="insert into printersinfo(printercount,printername,portname,createtime)\
                    values(\
                   (select COUNT(*)+1 from  printersinfo where createtime = (select max(createtime) from printersinfo )),\
                   '{0}',\
                   '{1}',\
                   (select max(createtime) from printersinfo )\
                   )".format(printerName,portName)
            cursor.execute(addsql)
            conn.commit()

"""对打印机状态是否进行监控"""
def updatePrinterCheckStatus(printerName,checkStatus):
    with pymssql.connect(databaseip, username, password, databasename) as conn:
        with conn.cursor() as cursor:
            updatesql = "update printersinfo set  checkstatus='{0}' where printername='{1}' and createtime = (select max(createtime) from printersinfo )".format(checkStatus, printerName)
            cursor.execute(updatesql)
            conn.commit()

