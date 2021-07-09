class LastMoveException(Exception):
    def __init__(self, string):
        super().__init__(string)
