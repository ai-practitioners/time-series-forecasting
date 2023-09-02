import polars as pl

def get_aggregate_data(dataframe, select_hierarchy):
    '''
        Aggregate sales data based on the specified hierarchy of "country," "state," or "city."
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