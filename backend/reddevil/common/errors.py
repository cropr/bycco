# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019


# all exception for the service layer
# mapped typicall the equivqlent HTTPException on the api level

class RdException(Exception):

    def __init__(self, status_code=500, description='Unknown'):
        self.status_code=status_code
        self.description= description


class RdBadRequest(RdException):

    def __init__(self, description='BadRequest'):
        super().__init__(status_code=400, description=description)


class RdNotAuthorized(RdException):
    def __init__(self, description='NotAuthorized'):
        super().__init__(status_code=401, description=description)



class RdNotFound(RdException):

    def __init__(self, description='NotFound'):
        super().__init__(status_code=404, description=description)


class RdInternalServerError(RdException):

    def __init__(self, description='InternalServerError'):
        super().__init__(description=description)
