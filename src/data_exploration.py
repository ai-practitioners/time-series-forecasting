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
    
def plot_sales_averages(dataframe, select_hierarchy, name):
    
    # create an aggregated dataframe based on user selection of either state or city
    agg_df = helper.get_aggregate_data(dataframe=dataframe, select_hierarchy=select_hierarchy)
    
    # check if date column is datetime datatype and sorted 
    if agg_df['date'].dtype != pl.Datetime:
        agg_df = agg_df.with_columns(pl.col('date').cast(pl.Datetime))
    else:
        pass
    
    # further subset the dataframe based on user selection of name of state or city
    sub_df = agg_df.filter(pl.col(select_hierarchy) == name)
    
    # create temporal averages
    sub_avg_df = (
        sub_df
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
            x=sub_avg_df['date'],
            y=sub_avg_df['sales'],
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
            x=sub_avg_df['date'],
            y=sub_avg_df['weekly_avg'],
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
            x=sub_avg_df['date'],
            y=sub_avg_df['monthly_avg'],
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
            x=sub_avg_df['date'],
            y=sub_avg_df['sales'],
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
            x=sub_avg_df['date'],
            y=sub_avg_df['quarterly_avg'],
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
            x=sub_avg_df['date'],
            y=sub_avg_df['yearly_avg'],
            name='Yearly Sales',
            line=dict(color='lime'),
            legendgroup='group2',
            hovertemplate='Yearly Sales: %{y}'
        ),
        row=2, col=1
    )

    # general customisation of the figure
    sales_fig.update_layout(
        title=f'Temporal Averages Sales by State<br>State: {sub_avg_df.item(row=0, column="state")}',
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