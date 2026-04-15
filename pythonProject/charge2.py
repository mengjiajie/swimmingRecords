import urllib2
import urllib
import json
from impala.dbapi import connect


# class LinkHive():
#     def __init__(self, host, port, username, password, database):
#         self.host = host
#         self.port = port
#         self.username = username
#         self.password = password
#         self.database = database
#

#     def __link(self):
#         self.conn = hive.Connection(host=self.host,
#                                     port=10000,
#                                     username=self.username,
#                                     password=self.password,
#                                     database=self.database,
#                                     auth='CUSTOM')
#         # CUSTOM  LDAP
#
#     def select_data(self, sql):
#         self.__link()
#
#         return pd.read_sql(sql, self.conn)


url = "https://base.tq-service.com/api/bill/third/chargeStatics/realTimeChargeStaticsNew"

pyload = {"enterpriseId": 107,
          "organizationId": 9790,
          "precinctId": 69579,
          "statisticType": "D",
          "month": "2022-06",
          "date": "2022-06-28"}
headers = {'content-type': "application/json"}
# data = urllib.urlencode(pyload)
request = urllib2.Request(url, json.dumps(pyload), headers=headers)
# response = urllib2.urlopen(request)
#
# print(response.read())

# res = response.json()
#
# print(res["resultData"]["precinctName"])
#
host = "139.155.112.99"
port = 10000
username = "hadoop"
password = "123456"
database = "hadoop_ind"

sql = "show databases"

conn = connect(host=host, port=10000, database=database, auth_mechanism='PLAIN')
cursor = conn.cursor()
cursor.execute(sql)
result = cursor.fetchone()
print(result)

#
# sql = "INSERT INTO table hadoop_ind.charge_real_time select " + "'" + res["resultData"]["precinctName"] + "'," \
#       + str(res["resultData"]["precinctId"]) + "," \
#       + str("100") + "," \
#       + str(res["resultData"]["housesNumber"]) + "," \
#       + str(res["resultData"]["mainBusinessArrearsAmount"]) + "," \
#       + str(res["resultData"]["mainBusinessAdvanceAmount"]) + "," \
#       + str(res["resultData"]["indirectSupplyWaterBillAmount"]) + "," \
#       + str(res["resultData"]["indirectSupplyElectricityBillAmount"]);
# print(" sql is \n " + sql)
# # res = link_hive.select_data(sql)
