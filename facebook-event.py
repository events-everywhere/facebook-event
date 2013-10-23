#!/usr/bin/env python3
# Simple command line script for creating, updating and 
# displaying Facebook events.

import argparse
import json
from datetime import datetime
from time import strftime, localtime
from facepy import GraphAPI


class FacebookEvent():
    '''API documentation:
    https://developers.facebook.com/docs/reference/api/event/
    '''
    
    def __init__(self, accessToken):
        self.graph = GraphAPI(accessToken)
    
    def create(self, name, start_time, **params):
        return self.graph.post('/events', name=name, start_time=start_time, 
                               privacy='OPEN', **params)
    
    def update(self, eventId, **params):
        fields = {}
        for param in params:
            if params[param]:
                fields[param] = params[param]
        return self.graph.post(eventId, **fields)
    
    def details(self, eventId):
        details, guests = ({}, {})
        
        event = self.graph.get(eventId)
        rsvps = self.graph.get(eventId + '/attending', 
                               fields='email,name,username')
        
        details['title'] = event['name']
        if 'description' in event:
            details['desc'] = event['description']
        for rsvp in rsvps['data']:
            if 'email' in rsvp:
                guests[rsvp['email']] = rsvp['name']
            elif 'username' in rsvp:
                guests[rsvp['username'] + '@facebook.com'] = rsvp['name']
            else:
                guests[rsvp['id']] = rsvp['name']
        details['guests'] = guests
        
        return details


def urlId(url):
    return url.rstrip('/').rsplit('/', 1)[-1]


def convertTime(dtStr):
    dtime = datetime.strptime(dtStr, '%Y-%m-%d %H:%M')
    return dtime.isoformat() + strftime('%z', localtime())


def readConfig(filePath):
    with open(filePath, 'r') as configFile:
        return json.loads(configFile.read())


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('action', choices=('create', 'update', 'details'), 
                           help='''use "create" to create a new event, 
                           "update" to update an event and 
                           "details" to get the event info''')
    argParser.add_argument('--title', help='event title')
    argParser.add_argument('--desc', help='event description')
    argParser.add_argument('--filedesc', type=argparse.FileType('r'), 
                           help='''path to the text file containing event 
                           description''')
    argParser.add_argument('--date', help='''event date, for example 
                           2013-11-11 16:16''')
    argParser.add_argument('--id', help='event id or event url')
    args = argParser.parse_args()
    
    config = readConfig('config.json')
    facebookEvent = FacebookEvent(config['accessToken'])
    
    if args.date:
        args.date = convertTime(args.date)
    if args.filedesc and not args.desc:
        args.desc = args.filedesc.read()
    if args.id:
        args.id = urlId(args.id)
    
    if args.action == 'create':
        event = facebookEvent.create(args.title, args.date, 
                                     description=args.desc)
        print('Created: https://www.facebook.com/events/' + event['id'])
    if args.action == 'update':
        facebookEvent.update(args.id, name=args.title, 
                             start_time=args.date, description=args.desc)
        print('Event updated.')
    if args.action == 'details':
        print(facebookEvent.details(args.id))

