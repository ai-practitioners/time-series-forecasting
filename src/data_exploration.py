from geopy import geocoders
from operator import itemgetter
from logger import logging

def get_geo_coordinates(username, location_name, country_code_iso):
    '''
        get latitude and longitude coordinates of a location using GeoNames
        
        step 1: poetry add geopy
        step 2: sign up for an account ->  https://www.geonames.org/login
        step 3: activate your account via the link sent to your email
        step 4: enable Free Web Services at https://www.geonames.org/manageaccount
        
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