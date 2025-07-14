import requests

BASE_URL = 'https://api.stlouisfed.org/fred/'
API_KEY = 'b1529de83b5821265a07082ece093ea2'

def fred_observation():
    '''
    Get observation time-series data from FRED.
    '''

    endpoint = 'series/observations'
    
    series_id = 'USRECD'
    file_type = 'json'
    start_date = '2000-01-01'
    end_date = '2025-01-01'
    ts_frequency = 'q'
    ts_units = 'pc1'

    obs_params = {
        'api_key':              API_KEY,
        'series_id':            series_id,
        'file_type':            file_type,
        'observation_start':    start_date,
        'observation_end':      end_date,
        'frequency':            ts_frequency,
        'units':                ts_units,
    }
    request = requests.get(BASE_URL + endpoint, params=obs_params)

if __name__ == '__main__':
    fred_observation()