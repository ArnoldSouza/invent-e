# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:32:47 2018

@author: Arnold
"""


# import modules
import funcs as fc  # import functions module


# get complements of information to build the chart
complements = fc.get_complements(conn,
                                 parameters,
                                 'product',
                                 'warehouse',
                                 'last_stock')


# add the recalculation of Stock Level Column
df = fc.cumulative_inverse_sum(df, complements['last_stock'])
