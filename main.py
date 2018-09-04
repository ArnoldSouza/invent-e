# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 02:37:42 2018

@author: Arnold
"""

from server.connection import DbConn  # lib to connect to the server
import pandas as pd  # import pandas dataframe
from utils.animation import CursorAnimation  # animated waiting cursor


db_data = DbConn('app_config.ini', 'ERP_SERVER')
db_data.connect_db()
df, parameters = db_data.sql_to_df('DATAFRAME', action=True)
complements = db_data.get_complements(parameters,
                                      'product',
                                      'warehouse',
                                      'last_stock')
db_data.close_db()

print('saving file...')

animation = CursorAnimation()  # Load Cursor
animation.start()  # Start Animation

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer, 'data')
writer.save()

animation.stop()  # Stop Animation

print(df.head())
