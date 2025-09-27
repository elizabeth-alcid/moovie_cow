import webbrowser
import requests
from urllib.parse import quote


# WatchMode API key and URL
API_KEY = "feRxwc91VirtXsLjJXf0Zm0an6eeG2eJDKQi1C5y"
API_URL = "https://api.watchmode.com/v1"

# Fallback pirating site - 123movies
FALLBACK = "https://ww20.0123movie.net/search.html?q={}"    
        
# Streaming Services
SERVICES = {
    'netflix': {
        'watchmode_id': 203,
        'search_url': 'https://www.netflix.com/search?q={}'},

    'hulu': {
        'watchmode_id': 157,
        'search_url': 'https://www.hulu.com/search?q={}'},

    'amazon-prime': {
        'watchmode_id': 26,
        'search_url': 'https://www.amazon.com/s?k={}&i=prime-instant-video'},

    'disney-plus': {
        'watchmode_id': 372,
        'search_url': 'https://www.disneyplus.com/search/{}'},

    'hbo-max': {
        'watchmode_id': 387,
        'search_url': 'https://www.max.com/'},

    'apple-tv': {
        'watchmode_id': 371,
        'search_url': 'https://tv.apple.com/search?term={}'},

    'paramount-plus': {
        'watchmode_id': 444,
        'search_url': 'https://www.paramountplus.com/search/{}'}
}

# Service priority - first available will be opened
SERVICE_QUEUE = [
    'hbo-max', 'hulu', 'disney-plus', 'amazon-prime', 
    'paramount-plus', 'netflix', 'apple-tv' ]
    

# Returns search results from title search API
def search_movie(movie_title):
    
    search_url = f"{API_URL}/search/"
    search_params = {
        'apiKey': API_KEY,
        'search_field': 'name',
        'search_value': movie_title
    }
    
    # Send GET request to URL
    response = requests.get(search_url, params = search_params)
    response.raise_for_status()
    search_results = response.json() # converts response to Python dictionary
    
    if not search_results.get('title_results'):
        return None # no movie found
    
    # Get the first result
    movie_id = search_results['title_results'][0]['id']

    # Second request to get details + sources
    details_url = f"{API_URL}/title/{movie_id}/details/"
    details_params = {
        'apiKey': API_KEY,
        'append_to_response': 'sources'
    }

    details_response = requests.get(details_url, params = details_params)
    details_response.raise_for_status()

    return details_response.json()
    
            

# Takes in a dictionary (first result from search_movie) and extracts the name of the service its available on from its details         
def get_available_service(movie_details):
    movie_id = movie_details['id']
    details_url = f"{API_URL}/title/{movie_id}/details/"
    search_params = {
        'apiKey': API_KEY, 
        'append_to_response': 'sources'
    }

    response = requests.get(details_url, params = search_params)
    response.raise_for_status()
    search_results = response.json() # returns dictionary with all details for that movie

    movie_source_ids = [source['source_id'] for source in search_results['sources']]

    for service_name in SERVICE_QUEUE:
        service_id = SERVICES[service_name]['watchmode_id']
        if service_id in movie_source_ids:
            return service_name

    return None  # not on any preferred service

    
# Open the movie on the preferred service
def open_movie(movie_title):
    movie_details = search_movie(movie_title)

    #print(movie_details['sources'])

    
    if not movie_details:
        webbrowser.open(FALLBACK.format(quote(movie_title)))
        return True

    # Returns the name of the first available preferred service
    service_name = get_available_service(movie_details)

    if service_name:
        direct_url = get_direct_url(movie_details, service_name)
        if direct_url:
            webbrowser.open(direct_url)
        else:
            service_url = SERVICES[service_name]['search_url'].format(quote(movie_title))
            webbrowser.open(service_url)
        return True

    webbrowser.open(FALLBACK.format(quote(movie_title)))
    return True

    
# Get direct URL from API if its available
def get_direct_url(movie_details, service_name):
    if 'sources' not in movie_details:
        return None
    
    service_id = SERVICES[service_name]['watchmode_id']
    
    for source in movie_details['sources']:
        if source.get('source_id') == service_id:
            # Try web_url first, then ios_url, then android_url
            return source.get('web_url') or source.get('ios_url') or source.get('android_url')
    
    return None