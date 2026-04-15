import pyhive
from pyhive import hive
import pandas as pd


class LinkHive(object):
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def __link(self):
        self.conn = hive.Connection(host=self.host,
                                    port=10000,
                                    username=self.username,
                                    password=self.password,
                                    database=self.database,
                                    auth='CUSTOM')
        # CUSTOM  LDAP

    def select_data(self, sql):
        self.__link()

        return pd.read_sql(sql, self.conn)

