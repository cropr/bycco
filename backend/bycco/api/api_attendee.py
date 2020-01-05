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
        ss = request.args.get('ss', None)
        cat = request.args.get('cat', None)
        format = request.args.get('format', 'json')
        if format == 'json':        
            return {'attendees': getAttendees(ss, cat)}
        elif format == 'csv':
            return {'attendees':getAttendeesCsv(ss, cat)}
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


