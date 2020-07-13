class OrderlyWebResponseError(Exception):
    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        self.response = response
        super(Exception, self).__init__(*args, **kwargs)

