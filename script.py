#!/usr/bin/env python

import stubhub_client

response = stubhub_client.search_events()

print 'Reported %d and got back %d' % (response['numFound'], len(response['events']))
for event in response['events']:
    print event
