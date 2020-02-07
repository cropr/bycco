# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource, request
from werkzeug.exceptions import BadRequest
from bycco.service import (
    addAttendee, 
    deleteAttendee,
    getAttendee,
    getAttendees,
    getAttendeesCsv,
    updateAttendee,
)

class AttendeesResource(Resource):
    
    def get(self):
        format = request.args.get('format', 'json')
        if format == 'json':        
            options = {}
            options['ss'] = request.args.get('ss', None)
            options['cat'] = request.args.get('cat', None)
            options['confirmed'] = request.args.get('confirmed', None)
            return {'attendees': getAttendees(options)}
        elif format == 'csv':
            return {'attendees':getAttendeesCsv()}
        else:
            return {'attendeees': []}



