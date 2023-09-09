from geopy import geocoders
from operator import itemgetter
from logger import logging

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