import requests
import polars as pl

BASE_URL = 'https://api.stlouisfed.org/fred/'
API_KEY = 'b1529de83b5821265a07082ece093ea2'

def plot_ts(df, name: str):
    chart = df.plot.line(
        x ='date', 
        y ='value'
    ).properties(
        width=500,
        height=250,
    )
    # chart.show()
    chart.save(f'./charts/{name}')

def response_handling(response, key):
    sc = response.status_code
    if sc == 200:
        js = response.json()[key]
        df = pl.DataFrame(js)
        return df
    else:
        print(f'Failed to retrieve data! {sc}')
        return pl.DataFrame()
    
def observations():
    '''
    Get observation time-series data from FRED.
    '''
    # Endpoint
    endpoint = 'series/observations'
    
    # Parameters
    series_id = 'CPIAUCSL'
    file_type = 'json'
    start_date = '2000-01-01'
    end_date = '2025-01-01'
    ts_frequency = 'q'
    ts_units = 'pca'
    params = {
        'api_key':              API_KEY,
        'series_id':            series_id,
        'file_type':            file_type,
        'observation_start':    start_date,
        'observation_end':      end_date,
        # 'frequency':            ts_frequency,
        'units':                ts_units,
    }

    # Request
    response = requests.get(BASE_URL + endpoint, params=params)

    # Response Handling
    df = response_handling(response, 'observations')
    if df.shape == (0,0): 
        return
    else:
        df = df.select(['date', 'value'])
        df = df.with_columns(
            pl.col('date').str.to_date(),
            pl.col('value').cast(pl.Float64),
        )
        return df

def category():
    '''
    Get category data from FRED API.
    '''
    # Endpoint
    endpoint = 'category'

    # Parameters
    file_type = 'json'
    category_id = 33913
    params = {
        'api_key': API_KEY,
        'file_type': file_type,
        'category_id': category_id,
    }

    # Request
    response = requests.get(BASE_URL + endpoint, params=params)

    # Response Handling
    return response_handling(response, 'categories')
    
def category_children():
    '''
    Get category children data from FRED API.
    '''
    # Endpoint
    endpoint = 'category/children'

    # Parameters
    file_type = 'json'
    category_id = 1
    params = {
        'api_key': API_KEY,
        'file_type': file_type,
        'category_id': category_id,
        # 'realtime_start': None,
        # 'realtime_end': None,
    }

    # Request
    response = requests.get(BASE_URL + endpoint, params=params)

    # Response Handling
    return response_handling(response, 'categories')

if __name__ == '__main__':
    obs = observations()
    cat = category()
    catc = category_children()

    print(obs)
    print(cat)
    print(catc)

    plot_ts(obs, 'test.png')