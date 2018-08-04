# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 02:37:42 2018

@author: Arnold
"""

from Server.connection import db_conn  # lib to connect to the server
import pandas as pd  # import pandas dataframe
from Utils.animation import CursorAnimation  # animated waiting cursor


db_data = db_conn('ENDICON_DATA')
db_data.connect()
df = db_data.sql_todf('Pré-notas', action=True)
db_data.close()

print('saving file...')

animation = CursorAnimation()  # Load Cursor
animation.start()  # Start Animation

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer, 'dados')
writer.save()

animation.stop()  # Stop Animation

print(df.head())
