# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:54:03 2018

@author: Arnold
"""

# from colorama import init, Fore  # colors to Windows Command Prompt

# init(autoreset=True)  # inicialize Windows Command Prompt
# e.g. print(Fore.YELLOW + 'some message')


def get_params(*args):
    """get variables parameters to a SQL Script"""
    param = {}
    print('-'*79)  # line delimiter
    for arg in args:
        if arg == 'filial':
            answer = get_input(msg='Insert subsidiary code:',
                               lenght=2,
                               type_val='numeric')
            param[arg] = "'{}'".format(answer)
        elif arg == 'armazem':
            answer = get_input(msg='Insert warehouse code:',
                               lenght=2,
                               type_val='numeric')
            param[arg] = "'{}'".format(answer)
        elif arg == 'codigo':
            answer = get_input(msg='Insert product code:',
                               lenght=8,
                               type_val='numeric')
            param[arg] = "'{}'".format(answer)
        elif arg == 'intervalo':
            answer = get_input(msg='Insert range [days]',
                               lenght=None,
                               type_val='numeric',
                               convert='int',
                               defalt='365')
            param[arg] = answer*-1
    print('\n', '-'*79, '\n', sep='')  # line delimiter
    return param


def get_input(msg, lenght, type_val, convert=None, defalt=None):
    """certifies a proper answer to parameters"""
    if defalt is not None:  # attach defalt value if exists
        value = input(msg + '[defalt: ' + str(defalt) + ']:')
        if value == '':
            value = defalt
    else:
        value = input(msg)  # get input
    value = value.strip()  # leave spaces behind
    value = value.lower()  # all letters lower case
    if value == '':
        raise Exception('String must to have lenght')
    if lenght is not None:  # numeric values doesn't have lenght
        if len(value) != lenght:
            raise Exception('String out of lenght. Limit: {}, Current: {}.'
                            .format(lenght, len(value)))
    if type_val == 'numeric':
        if value.isnumeric() is not True:
            raise Exception('String is not only numeric')
    elif type_val == 'alphabets':
        if value.isalpha() is not True:
            raise Exception('String is not only alphabets')
    if convert is not None:  # convert the value of the input
        if convert == 'int':
            value = int(value)
    return value


def get_complements(conn, parameters, *args):
    """get the more information about some details"""
    answer = {}
    for arg in args:
        if arg == 'product':
            sqlScrpt = """
            SELECT
                RTRIM(SB1010.B1_COD)+' - '+RTRIM(SB1010.B1_DESC)
            FROM PROTHEUS.dbo.SB1010 SB1010
            WHERE
                SB1010.D_E_L_E_T_<>'*' AND
                SB1010.B1_COD = {}
            """.format(parameters['codigo'])
            query = get_data(conn, sqlScrpt)
            if query is None:
                answer[arg] = 'Not Found'
            else:
                answer[arg] = query
            print('product:', answer[arg])
        if arg == 'warehouse':
            sqlScrpt = """
            SELECT
                RTRIM(Z01010.Z01_CODGER)+' - '+RTRIM(Z01010.Z01_DESC)
            FROM PROTHEUS.dbo.Z01010 Z01010
            WHERE
                Z01010.D_E_L_E_T_<>'*' AND
                Z01010.Z01_FILIAL = {} AND
                Z01010.Z01_COD = {}
            """.format(parameters['filial'], parameters['armazem'])
            query = get_data(conn, sqlScrpt)
            if query is None:
                answer[arg] = 'Not Found'
            else:
                answer[arg] = query
            print('warehouse:', answer[arg])
        if arg == 'last_stock':
            sqlScrpt = """
            SELECT
                SB2010.B2_QATU
            FROM PROTHEUS.dbo.SB2010 SB2010
            WHERE
                SB2010.D_E_L_E_T_<>'*' AND
                SB2010.B2_FILIAL = {} AND
                SB2010.B2_LOCAL = {} AND
                SB2010.B2_COD = {}
            """.format(parameters['filial'],
                       parameters['armazem'],
                       parameters['codigo'])
            query = get_data(conn, sqlScrpt)
            if query is None:
                print('actual stock not found, assigning ZERO...')
                answer[arg] = 0
            else:
                answer[arg] = query
            print('actual stock:', answer[arg])
    return answer


def cumulative_inverse_sum(df, last_stock):
    """calculate the stock of the past days given
    the current stock level and add it to dataframe"""
    # calculate the cumulative sum of moviments
    cumulative_sum = (df.SOMA_ENTRA + df.SOMA_SAI).cumsum()
    # Subtract the diference of the stock variation between the
    # actual stock (last_stock)and the last value of stock from
    # the cumulative sum
    df["STOCK"] = cumulative_sum - (cumulative_sum.iloc[-1] - last_stock)
    return df
