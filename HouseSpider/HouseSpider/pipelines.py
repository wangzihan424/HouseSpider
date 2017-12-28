# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HousespiderPipeline(object):
    def process_item(self, item, spider):
        return item


import xlsxwriter

class ExcelPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook("new_house.xlsx")
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, u"楼盘")
        self.worksheet.write(0, 1, u"面积")
        self.worksheet.write(0, 2, u"地址")
        self.worksheet.write(0, 3, u"价钱")
        self.worksheet.write(0, 4, u"几手")
        # self.title_list = []
        # self.address_list = []
        # self.flood_list = []
        # self.money_list = []
        # self.type_list = []
        self.wz = []



    def process_item(self, item, spider):

        # title = item['title']
        # self.title_list.append(title)
        #
        # address = item['address']
        # self.address_list.append(address)
        #
        # flood = item['flood']
        # self.flood_list.append(flood)
        #
        # type = item['style']
        # self.type_list.append(type)
        #
        # money = item['money']
        # self.money_list.append(money)
        title = item['title']
        address = item['address']
        flood = item['flood']
        type = item['style']
        money = item['money']

        a_list = [title,address,flood,money,type]
        # a_list.append(title)
        # a_list.list.append(address)
        # a_list.list.append(flood)
        # a_list.list.append(type)
        # a_list.list.append(money)

        self.wz.append(a_list)
        return item

    def __del__(self):
        # self.worksheet.write_column("A2", self.title_list)
        # self.worksheet.write_column("B2", self.address_list)
        # self.worksheet.write_column("C2", self.flood_list)
        # self.worksheet.write_column("D2", self.money_list)
        # self.worksheet.write_column("E2", self.type_list)

        # self.worksheet.write_row("A%s" % str(len(self.list)),self.list)
        # for x in xrange(2,len(self.list)):
        #     self.worksheet.write("A%s"%str(x),self.list)
        col = 0
        row = 1
        for cost in (self.wz):
            self.worksheet.write_row(row, col, cost)
            row += 1
        self.workbook.close()


from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi
#MySQL 可以通过"连接池"实现异步写入
class MySQLAsynPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
        query = self.dbpool.runInteraction(self.create_table)
    def create_table(self,cursor):
        sql="create table  if not exists house(id INT PRIMARY KEY auto_increment not NULL ,house_name VARCHAR (255) not NULL ,address VARCHAR (255), mianji VARCHAR (255),money VARCHAR (255),style VARCHAR (255) )"
        cursor.execute(sql)
    @classmethod
    def from_settings(cls,settings):
        host = settings['MYSQL_HOST']
        name = settings['MYSQL_USERNAME']
        psw = settings['MYSQL_PASSWORD']
        port = settings['MYSQL_PORT']
        charset = settings['MYSQL_CHARSET']
        db = settings['MYSQL_DB']
        #参数1 : dbapiName 数据库接口名称
        #参数2 : *connargs
        #参数3 : **connkw
        dbpool=adbapi.ConnectionPool("MySQLdb",host=host, user=name, passwd=psw, db=db, use_unicode=True,charset=charset,port=port,cursorclass=DictCursor)
        return cls(dbpool)
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_sql,item)
        query.addErrback(self.insert_err)
        return item
    def insert_err(self,failed):
        print ">>>>>>>>>>>>>>>>",failed
    def insert_sql(self,cursor,item):
        sql = "insert into house(house_name,address,mianji,money,style) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(item['title'],item['address'],item['flood'],item['money'],item['style']))



