# -*- coding: utf-8 -*-
"""
Created on 12/10/2018
As a part of invente

@author: Arnold Souza
email: arnoldecs@hotmail.com
https://github.com/ArnoldSouza
"""

# imports
import pickle  # used to save objects

# package import
from server.connection import DbConn  # lib to connect to the server
from utils.data_modeling import cumulative_inverse_sum  # recalculate stock
from plot.movigrama_dashboard import assembly_chart  # assembly bokeh chart
from utils.time_stamp import timing  # decorator to get elapsed time


@timing
def exec_script():
    # open database connection
    db_data = DbConn('app_config.ini', 'ERP_SERVER')
    db_data.connect_db()
    # query the database server
    df, parameters = db_data.sql_to_df('sql_movigrama', action=True)

    # get complements of information to build the chart
    complements = db_data.get_complements(parameters,
                                          'product',
                                          'warehouse',
                                          'last_stock')
    # close the database connection
    db_data.close_db()

    # add the recalculation of Stock Level Column
    df = cumulative_inverse_sum(df, complements['last_stock'])

    # save the dataframe into pickle file
    df.to_pickle('_pickled\data.pkl')
    pickle.dump(complements, open("_pickled\complements.pkl", "wb"))  # TODO create a class of pickle

    # function to plot the graph
    assembly_chart(df, complements)


while True:
    print('●'*79)  # line delimiter
    print('Stock Movement analysis - Movigrama')
    print('●'*79)  # line delimiter
    exec_script()
