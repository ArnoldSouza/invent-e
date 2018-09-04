
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

# add the recalculation of Stock Level Column
# df = fc.cumulative_inverse_sum(df, complements['last_stock'])
