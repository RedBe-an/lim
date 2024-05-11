class unexpectedInputError(Exception) :
    def __init__(self, message) :
        super.__init__(f"unexpected input error : {message}")

class notExistError(Exception) :
    def __init__(self, message) :
        super.__init__(f"not exist error : {message}")