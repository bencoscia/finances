#!/usr/bin/env python

"""
Columns in SQL database: name, account, price, number

Accounts: TD_Ameritrade_IRA
          TD_Ameritrade_Personal
          Robinhood
          Fidelity
"""


import argparse
import os
import sqlite3 as sql
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def initialize():

    parser = argparse.ArgumentParser(description='Get various summaries of owned stock by interacting with an SQL '
                                                 'database')
    parser.add_argument('-db', '--database', type=str, default='stocks.db', help='Name of database which contains'
                                                                                 'stock information')
    parser.add_argument('-t', '--tablename', type=str, default='stock_info', help='Name of table containing stock'
                                                                                  'information')

    return parser


class StockInfo(object):

    def __init__(self, database, tablename):

        self.tablename = tablename
        self.connection = sql.connect("%s/%s" % (location, database))  # connect to database
        self.crsr = self.connection.cursor()  # object for executing sql queries

        self.prices = {}
        self.database_name = database

    def update_prices(self):

        command = "SELECT DISTINCT name FROM %s" % self.tablename  # get names of stocks
        names = [i[0] for i in self.crsr.execute(command).fetchall()]

        for name in names:
            if name != 'cash':
                self.prices[name] = si.get_live_price(name)
                update = "UPDATE %s SET price = %.6f WHERE name = '%s'" %(self.tablename, self.prices[name], name)
                self.crsr.execute(update)

        self.connection.commit()
        print('Stock prices updated in %s' % self.database_name)

    def retirement(self, account='TD_Ameritrade_IRA'):

        command = "SELECT name, number, price FROM %s WHERE account = '%s'" % (self.tablename, account)
        output = self.crsr.execute(command).fetchall()

        values = {}
        for i in range(len(output)):
            values[output[i][0]] = float(output[i][1])*float(output[i][2])

        print(values)

if __name__ == "__main__":

    args = initialize().parse_args()

    stocks = StockInfo(args.database, args.tablename)
    #stocks.update_prices()
    stocks.retirement()


