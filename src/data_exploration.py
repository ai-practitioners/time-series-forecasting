from geopy import geocoders
from operator import itemgetter
from logger import logging
import helper as helper
import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_geo_coordinates(username, location_name, country_code_iso):
    '''
        Retrieve latitude and longitude coordinates of a location using the GeoNames geocoder service.

        This function queries the GeoNames geocoder service to obtain geographical information (latitude and longitude)
        for a specified location name and country code ISO. To use this function, follow the the steps below:
        
        step 1: poetry add geopy
        step 2: sign up for an account ->  https://www.geonames.org/login
        step 3: activate your account via the link sent to your email
        step 4: enable Free Web Services at https://www.geonames.org/manageaccount

        Args:
            username (str): Your GeoNames username for authentication.
            location_name (str): The name of the location for which you want to obtain coordinates.
            country_code_iso (str): The ISO country code (e.g., 'US' for the United States) of the location.

        Returns:
            tuple or None: A tuple containing latitude and longitude values as floats (lat, lng), or None if the location
            is not found or if there is an error during the process.

        Note:
            - To use this function, you need to install the 'geopy' library by running 'poetry add geopy'.
            - Ensure that you have signed up for a GeoNames account and completed the necessary steps mentioned in the docstring.

        Example:
            coordinates = get_geo_coordinates(username='your_username', location_name='New York', country_code_iso='US')
            if coordinates:
                print(f'Coordinates: Latitude {coordinates[0]}, Longitude {coordinates[1]}')
            else:
                print('Location not found or error occurred.')
    
    '''
    
    try:
        
        logging.info(f'Getting geographical information for {location_name}.')
        
        # create an instance of GeoNames geocoder and specify username for auth
        gn = geocoders.GeoNames(username=username)

        # obtain geographical information for a given query
        location = gn.geocode(query=location_name, country=country_code_iso)
        
        # if location is found, return lat and long values from location.raw dictionary
        if location:
            
            logging.info(f'Geographical information for {location_name} found. Returning latitutde and longitude values.')
            
            # extract latitude and longitude from location.raw dictionary
            return itemgetter('lat', 'lng')(location.raw)
        else:
            print(
                f'Location name {location_name} not found in {country_code_iso} for username {username}. '
                f'Please check all information and try again.'
            )
            return None
    
    except Exception as e:
        print(e)
        return None
    
def plot_sales_averages(dataframe, select_hierarchy, name=None):
    '''
        This function plots the sales averages for a given hierarchy (country, state, or city) from a provided dataframe.

        Parameters:
            - dataframe (polars.DataFrame): The input dataframe containing sales data.
            - select_hierarchy (str): The hierarchy level to aggregate data on. This can be 'country', 'state', or 'city'.
            - name (str, optional): The specific name of the state or city to plot data for. This should be None when select_hierarchy is 'country'.

        Raises:
            ValueError: If 'name' is not None when 'select_hierarchy' is 'country'.
            ValueError: If an invalid state name is provided when 'select_hierarchy' is 'state'.
            ValueError: If an invalid city name is provided when 'select_hierarchy' is 'city'.

        Returns:
            None. The function directly plots the sales averages using Plotly.
    '''
    
    if select_hierarchy == 'country':
        # check if name is set to None or left empty when select_hierarchy is 'country'
        if name is not None:
            raise ValueError('Ignore name or set it to None when select_hierarchy is "country".')
    
    # create an aggregated dataframe based on user selection of either state or city
    agg_df = helper.get_aggregate_data(dataframe=dataframe, select_hierarchy=select_hierarchy)
    
    # check if date column is datetime datatype and sorted 
    if agg_df['date'].dtype != pl.Datetime:
        agg_df = agg_df.with_columns(pl.col('date').cast(pl.Datetime))
    else:
        pass
       
    # check if the name of city or state is valid
    if select_hierarchy == 'state':
        # get a list of name of states
        valid_states = dataframe.select('state').unique().to_series().to_list()
        
        if name not in valid_states:
            raise ValueError(f'Invalid state name. Please choose one of the following: {valid_states}')
        
    elif select_hierarchy == 'city':
        # get a list of name of cities
        valid_cities = dataframe.select('city').unique().to_series().to_list()
        
        if name not in valid_cities:
            raise ValueError(f'Invalid city name. Please choose one of the following: {valid_cities}')
    
    else:
        # no checks needed if select_hierarchy == 'country'
        pass
    
    if select_hierarchy == 'country':
        agg_df = agg_df
    else:
        # further subset the dataframe based on user selection of name of state or city
        agg_df = agg_df.filter(pl.col(select_hierarchy) == name)
       
    # create temporal averages
    tmp_avg_df = (
        agg_df
        .with_columns(
            weekly_avg=pl.col('sales').rolling_mean(window_size='1w', by='date', closed='left')
        )
        .with_columns(
            monthly_avg=pl.col('sales').rolling_mean(window_size='1mo_saturating', by='date', closed='left')
        )
        .with_columns(
            quarterly_avg=pl.col('sales').rolling_mean(window_size='1q_saturating', by='date', closed='left')
        )
        .with_columns(
            yearly_avg=pl.col('sales').rolling_mean(window_size='1y_saturating', by='date', closed='left')
        )    
    )
    
    # create a figure with two subplots
    sales_fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            'Actual vs Weekly/Monthly Avg',
            'Actual vs Quaterly/Yearly Avg',
        )
    )

    # add actual trace to the top subplot
    sales_fig.add_trace(
        go.Scatter(
            x=tmp_avg_df['date'],
            y=tmp_avg_df['sales'],
            name='Actual Sales (Weekly/Monthly)',
            line=dict(color='cyan'),
            legendgroup='group1',
            hovertemplate='Actual Sales (Weekly/Monthly): %{y}'
        ),
        row=1, col=1,
    )

    # add weekly avg trace to the top subplot
    sales_fig.add_trace(
        go.Scatter(
            x=tmp_avg_df['date'],
            y=tmp_avg_df['weekly_avg'],
            name='Weekly Sales',
            line=dict(color='magenta'),
            legendgroup='group1',
            hovertemplate='Weekly Sales: %{y}'
        ),
        row=1, col=1
        
    )

    # add monthly trace to the top subplot
    sales_fig.add_trace(
        go.Scatter(
            x=tmp_avg_df['date'],
            y=tmp_avg_df['monthly_avg'],
            name='Monthly Sales',
            line=dict(color='yellow'),
            legendgroup='group1',
            hovertemplate='Monthly Sales: %{y}'
        ),
        row=1, col=1
    )

    # add actual trace again to the bottom subplot
    sales_fig.add_trace(
        go.Scatter(
            x=tmp_avg_df['date'],
            y=tmp_avg_df['sales'],
            name='Actual Sales (Quarterly/Yearly)',
            line=dict(color='cyan'),
            legendgroup='group2',
            hovertemplate='Actual Sales (Quarterly/Yearly): %{y}'
        ),
        row=2, col=1,
    )

    # add quarterly avg trace to the bottom subplot
    sales_fig.add_trace(
        go.Scatter(
            x=tmp_avg_df['date'],
            y=tmp_avg_df['quarterly_avg'],
            name='Quaterly Sales',
            line=dict(color='orange'),
            legendgroup='group2',
            hovertemplate='Quaterly Sales: %{y}'
        ),
        row=2, col=1
    )

    # add yearly avg trace to the bottom subplot
    sales_fig.add_trace(
        go.Scatter(
            x=tmp_avg_df['date'],
            y=tmp_avg_df['yearly_avg'],
            name='Yearly Sales',
            line=dict(color='lime'),
            legendgroup='group2',
            hovertemplate='Yearly Sales: %{y}'
        ),
        row=2, col=1
    )

    # change figure title for different hierarchy selection
    if select_hierarchy == 'country':
        figure_title = f'Temporal Averages Sales<br>Ecuador'
    elif select_hierarchy == 'state':
        figure_title = f'Temporal Averages Sales by State<br>State: {tmp_avg_df.item(row=0, column=select_hierarchy)}'
    else:
        figure_title = f'Temporal Averages Sales by City<br>City: {tmp_avg_df.item(row=0, column=select_hierarchy)}'
    
    # general customisation of the figure
    sales_fig.update_layout(
        title=figure_title,
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        plot_bgcolor='Black',
        paper_bgcolor='Black',
        font=dict(
            color='White',
            size=12
        ),
        yaxis=dict(
            title='Value',
            tickprefix='$',
            showgrid=True,
            gridcolor='Darkgrey'
        ),
        xaxis=dict(
            title='Date',
            # tickangle=-20,
            dtick='M1',
            tickformat='%b\n%Y'
        ),
        autosize=True,
        height=900
    )

    # give x-axes a proper month format
    sales_fig.update_xaxes(
        title_text='Date',
        dtick='M1',
        tickformat='%b\n%Y',
        showgrid=False,
        row=2, col=1
    )

    # give y-axes a proper dollar format
    sales_fig.update_yaxes(
        title_text='Value',
        tickprefix='$',
        row=2, col=1
    )

    # manually add legends
    sales_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.4, y=1,
        text="<span style='font-size:12px;color:cyan'>●</span> Actual Sales",
        showarrow=False
    )

    sales_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1,
        text="<span style='font-size:12px;color:magenta'>●</span> Weekly Avg Sales",
        showarrow=False
    )

    sales_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.61, y=1,
        text="<span style='font-size:12px;color:yellow'>●</span> Monthly Avg Sales",
        showarrow=False
    )

    sales_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.4, y=0.36,
        text="<span style='font-size:12px;color:cyan'>●</span> Actual Sales",
        showarrow=False
    )

    sales_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=0.36,
        text="<span style='font-size:12px;color:orange'>●</span> Quarterly Avg Sales",
        showarrow=False
    )

    sales_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.61, y=0.36,
        text="<span style='font-size:12px;color:lime'>●</span> Yearly Avg Sales",
        showarrow=False
    )

    return sales_fig.show()

def plot_stores_inventory(dataframe):
    '''
        Generate an inventory heatmap to visualize product distribution among
        stores.

        Parameters:
            dataframe (polars.DataFrame): Input DataFrame containing store
            inventory data.

        Returns:
            None (Displays the heatmap using Plotly).
    '''
    
    # get a list of all family names
    all_family_names = (
        dataframe
        .select('family')
        .unique()
        .to_series()
        .to_list()
    )

    # group the data by store number and get unique family names that each store is selling
    grouped = (
        dataframe
        .group_by('store_nbr')
        .agg(pl.col('family').alias('family_sold'))
    )

    # create a new column family_not_sold
    grouped = grouped.with_columns(
        # select family_sold and apply the following function
        pl.col('family_sold')
        
        # function - create a list of items that are not in the family_sold list
        .map_elements(lambda x: [item for item in all_family_names if item not in x])
        
        # assign a new name to the new column
        .alias('family_not_sold')
    )

    # sort the dataframe by store number
    grouped = grouped.sort('store_nbr')

    # sorted list of store numbers
    store_numbers = grouped['store_nbr'].to_list()
    
    # create a binary matrix indicating whether a store sells a family product
    matrix = []
    for family_list in grouped['family_sold']:
        row = [1 if family_name in family_name else 0 for family_name in all_family_names]
        matrix.append(row)
    
    # create the inventory heatmap
    fam_invent_fig = go.Figure(
    data=go.Heatmap(
        z=matrix,
        x=all_family_names,
        y=store_numbers,
        autocolorscale=True,
        hoverongaps=False,
        showscale=False
        )
    )

    # customize the appearance of the heatmap
    fam_invent_fig.update_xaxes(
        title='Family Names',
        tickangle=-45,
    )

    fam_invent_fig.update_yaxes(
        title='Store Number',
        type='category',
        tickmode='array',
        tickvals=store_numbers,
        ticktext=store_numbers,
        tickfont=dict(size=10),
    )

    fam_invent_fig.update_layout(
        title='Inventory Heatmap (All Stores)',
        template='plotly_dark',
        height=800,
    )

    # return the heatmap
    return fam_invent_fig.show()