import polars as pl
from logger import logging

def query_clean_up(dataframe):
    '''
        Perform data cleaning on a SQL query output DataFrame.

        This function aims to clean and preprocess a DataFrame generated from a SQL query output. It addresses specific cleaning
        tasks such as replacing values, handling null values, and more.

        Args:
            dataframe (polars.DataFrame): The input DataFrame to be cleaned.

        Returns:
            polars.DataFrame: A cleaned and processed DataFrame.

        Raises:
            Exception: If any unexpected error occurs during the cleaning process, it is logged as an error message.
                        The cleaning process is designed to handle various data anomalies gracefully.
    '''
    
    try:
        logging.info("Initialising unique data cleaning of sql query output")
        
        # change 'Additional,Transfer' to 'Additional'
        # due to a limitation during sql query in CTE CityHolidays
        dataframe = dataframe.with_columns(pl.col('city_hols_type').str.replace('Additional,Transfer', 'Additional'))
        
        # list all holidays type columns
        hols_type_cols = ['city_hols_type', 'state_hols_type', 'nation_hols_type']
        
        # replace null values with NotHoliday
        replacement_value = 'NotHoliday'

        # iterate over each column and change null values to 'NotHoliday'
        for col in hols_type_cols:
            dataframe = dataframe.with_columns(
                pl
                .when(dataframe[col].is_null())     # check if a value in the column is null
                .then(pl.lit(replacement_value))    # replace null values with 'NotHoliday'
                .otherwise(dataframe[col])           # keep non-null values as they are
                .alias(col)                         # give the column back the same name
            )
            
        logging.info("Clean up successful!")
        
    except Exception as e:
        logging.error(f"Clean up failed: {e}")

    return dataframe


def shrink_dataframe(dataframe):
    '''
        Reduce memory usage by downcasting each column in a DataFrame to the smallest possible data type based on column statistics.

        This function aims to optimize memory usage by downcasting data types for each column in the input DataFrame. It calculates
        the minimum and maximum values for numeric columns and selects the smallest possible data type that can represent the range
        without loss of precision. String columns are not modified.

        Args:
            dataframe (polars.DataFrame): The input DataFrame to be memory-optimized.

        Returns:
            polars.DataFrame: A memory-optimized DataFrame with downcasted data types.

        Raises:
            Exception: If any unexpected error occurs during the optimization process, it is logged as an error message.
                        The optimization process is designed to handle various data anomalies gracefully.

        Note:
            This function can significantly reduce memory usage for large DataFrames with numeric columns.
    '''
    
    try:
        logging.info(f"Shrinking dataframe to reduce memory. Size of dataframe: {round(dataframe.estimated_size('mb'),2)} MB")
        
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
        
        logging.info(f"Shrink operation successful. Size of dataframe reduce to: {round(dataframe.estimated_size('mb'),2)} MB")
            
    except Exception as e:
        logging.error(f"Shrink dataframe failed: {e}")
    
    return dataframe
    