class AuthServiceException(Exception):
    def __init__(self, message, status_code, error_code, details=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details