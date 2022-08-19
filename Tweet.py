class Tweet:
    _message = ""
    _lang = ""
    _id = ""

    def __init__(self):
        pass

    @property
    def message(self):  # this is getter for module
        return self._message

    @message.setter
    def message(self, m):
        self._message = m

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, m):
        self._lang = m

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, m):
        self._id = m

