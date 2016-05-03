from flask import Flask, jsonify
from operator import itemgetter
import dateutil.parser
import stubhub_client

app = Flask(__name__)

def get_stripped_event(event):
    return {'url': event['eventInfoUrl'],
            'date': dateutil.parser.parse(event['dateLocal']).strftime('%a, %b %d'),
            'minPrice': event['ticketInfo']['minPrice'],
            'id': event['id']}

@app.route('/')
def hello_world():
    response = stubhub_client.search_events()

    events = response['events']

    stripped_events = [get_stripped_event(event) for event in events]
    sorted_events = sorted(stripped_events, key=itemgetter('minPrice'))

    return jsonify(events=sorted_events)

@app.route('/events/<event_id>')
def event(event_id):
    response = stubhub_client.get_inventory(event_id)

    # events = response['events']
    # stripped_events = [get_stripped_event(event) for event in events]
    # sorted_events = sorted(stripped_events, key=itemgetter('minPrice'))

    return jsonify(response)

@app.route('/alerts')
def my_alerts():
    response = stubhub_client.user_alerts()
    return jsonify(response)

@app.route('/create_alert')
def create_alert():
    response = stubhub_client.create_alert()
    return jsonify(response)

if __name__ == '__main__':
    # TODO(holman): make this dev only
    app.run(debug=True)
