class DocumentServiceException(Exception):
    def __init__(self):
        self.status_code = 420
        self.message="error working on it"
        self.error_code=420
        self.details="working on it.."
