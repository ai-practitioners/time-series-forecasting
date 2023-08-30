import polars as pl


def shrink_dataframe(dataframe):
    '''
        takes in a dataframe and downcast each column to the smallest dtype
        based on column min and max range.
    '''
    
    # iterate through each column in the dataframe
    for column_name in dataframe.columns:
        
        column = dataframe[column_name]
        
        # initialise an empty downcast type for each loop
        downcast = None
        
        # downcast logic for Int columns
        if column.dtype == pl.Int64:
            column_min = column.min()
            column_max = column.max()
            
            if column_min >= -128 and column_max <= 127:
                downcast = pl.Int8
            elif column_min >= -32_767 and column_max <= 32_767:
                downcast = pl.Int16
            elif column_min >= -2_147_483_647 and column_max <= 2_147_483_647:
                downcast = pl.Int32
            else:
                downcast = None
                
        # downcast logic for Float column
        elif column.dtype == pl.Float64: 
            column_min = column.min()
            column_max = column.max()
            
            if column_min >= -3.4028235e+38 and column_max <= 3.4028235e+38:
                downcast = pl.Float32
            else:
                downcast = None
        
        # no downcast for string columns
        else:
            pass
                
        # where any of the above condition is met, downcast operation applies
        if downcast:
            dataframe = dataframe.with_columns(column.cast(dtype=downcast))
        else:
            pass
    
    return dataframe
    