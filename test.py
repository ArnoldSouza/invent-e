# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:32:47 2018

@author: Arnold
"""


# import modules
import funcs as fc  # import functions module


# TODO delete in future
#parameters = {'filial': "'02'",
#              'armazem': "'21'",
#              'codigo': "'02500727'",
#              'intervalo': -365}

# put values into variables of the SQL query
# TODO uncomment in future
parameters = fc.get_params('filial',
                           'armazem',
                           'codigo',
                           'intervalo')

# Open and read the file as a single buffer
sqlFile = fc.read_sql_file('DATAFRAME')

File = sqlFile.format(**parameters)

# open database connection
conn = fc.connect()

# query the database server
df = fc.fetch_data(sqlFile, conn, action=False)  # TODO remember change action

# get complements of information to build the chart
complements = fc.get_complements(conn,
                                 parameters,
                                 'product',
                                 'warehouse',
                                 'last_stock')

# close the database connection
conn.close_db()

# add the recalculation of Stock Level Column
df = fc.cumulative_inverse_sum(df, complements['last_stock'])
