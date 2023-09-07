import polars as pl

def get_aggregate_data(dataframe, select_hierarchy):
    '''
        Aggregate sales data based on the specified hierarchy of "country," "state," or "city."

        Parameters:
        - dataframe (pl.DataFrame): The input DataFrame containing sales data.
        - select_hierarchy (str): The hierarchy level for aggregation, one of "country," "state," or "city."

        Returns:
        - pl.DataFrame: A DataFrame containing aggregated sales data based on the selected hierarchy.

        Raises:
        - ValueError: If the provided select_hierarchy is not one of "country," "state," or "city."

        Example:
        ```
        # Aggregate sales data by state
        state_agg_data = get_aggregate_data(sales_data, "state")
        ```
    '''

    # define sorting hierarchy as dictionary
    sort_hierarchy = {
        'country': ['date'],
        'state': ['state', 'date'],
        'city': ['city', 'date']
    }
    
    # check if select_hierarchy is valid
    if select_hierarchy not in sort_hierarchy:
        raise ValueError('Invalid sort hierarchy selection. Please choose one of "country", "state" or "city".')
    
    # retrieve grouping list based on user selection
    hierarchy_selection = sort_hierarchy.get(select_hierarchy)

    # aggregation calculation by sort hierarchy selectiong
    agg_df = (
        dataframe
        .group_by(by=hierarchy_selection)
        .agg(pl.col('sales').sum())
        .sort(by=hierarchy_selection)
    )
    
    return agg_df