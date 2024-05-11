
class unexpectedInputError(Exception) :
    def __init__(self, message) :
        super.__init__(f"unexpected input error : {message}")