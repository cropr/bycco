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

    def post(self):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')

class AttendeeResource(Resource):
    
    def delete(self, id:str):
        pass

    def get(self, id:str):
        pass

    def put(self, id:str):
        pass


