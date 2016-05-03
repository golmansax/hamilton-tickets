import base64
import requests
from os import getenv

DOMAIN='https://api.stubhub.com'
APPLICATION_TOKEN=getenv('STUBHUB_PROD_APPLICATION_TOKEN')
USER_TOKEN=getenv('STUBHUB_USER_TOKEN')
CONSUMER_KEY=getenv('STUBHUB_PROD_CONSUMER_KEY')
CONSUMER_SECRET=getenv('STUBHUB_PROD_CONSUMER_SECRET')
MY_USERNAME=getenv('STUBHUB_USERNAME')
MY_PASSWORD=getenv('STUBHUB_PASSWORD')
MY_USER_ID=getenv('STUBHUB_USER_ID')

HEADERS = {
    'Authorization': 'Bearer %s' % USER_TOKEN,
    'Accept': 'application/json',
    'Accept-Encoding': 'application/json',
    'Content-Type': 'application/json'}

def search_events():
    url = '%s/search/catalog/events/v2' % DOMAIN
    params = { 'performerId': '1500227',
            'title': '-PARKING',
            'status': 'active',
            'maxPrice': 600.0,
            'limit': 100}
    raw_response = requests.get(url, headers=HEADERS, params=params)
    return raw_response.json()

def get_inventory(event_id):
    url = '%s/search/inventory/v1' % DOMAIN
    params = { 'eventid': event_id }
    raw_response = requests.get(url, headers=HEADERS, params=params)
    return raw_response.json()

def user_alerts():
    url = '%s/user/customers/v1/%s/pricealerts' % (DOMAIN, MY_USER_ID)

    raw_response = requests.get(url, headers=HEADERS)
    return raw_response.json()

def raw_login_response():
    url = '%s/login' % DOMAIN

    encoded = base64.b64encode('%s:%s' % (CONSUMER_KEY, CONSUMER_SECRET))
    headers = HEADERS.copy()
    headers['Authorization'] = 'Basic %s' % encoded

    data = {
        'grant_type': 'password',
        'username': MY_USERNAME,
        'password': MY_PASSWORD,
        'scope': 'PRODUCTION'}

    return requests.post(url, data=data, headers=headers)

def get_tokens():
    return raw_login_response().json()

def get_user_id():
    return raw_login_response().headers['X-StubHub-User-GUID']

def create_alert():
    url = '%s/user/customers/v1/%s/pricealerts' % (DOMAIN, MY_USER_ID)
    EVENT_ID = '9441730'
    price_data = {
            'eventId': EVENT_ID,
            'maxTicketPrice': {'amount': '600.0', 'currency': 'USD'},
            'quantity': '2'}

    data = {'priceAlert': price_data}

    raw_response = requests.post(url, json=data, headers=HEADERS)
    return raw_response.json()
