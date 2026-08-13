class UserAbortException(Exception):
    """Exception raised when the user aborts an operation."""

    def __init__(self, message: str = "The user aborted the operation."):
        self.message = message
        super().__init__(self.message)
