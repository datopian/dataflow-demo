class DataResource(object):
    def __init__(self, streamOrArray, schema=None, metadata=None):
        if isinstance(streamOrArray, DataResource):
            # HACK
            self.__dict__ = streamOrArray.__dict__
        else:
            self.buffer_ = streamOrArray
            self.descriptor = metadata or {}
            self.descriptor['schema'] = schema

    @property
    def schema(self):
        return self.descriptor['schema']

    @property
    def path(self):
        return self.descriptor['path']

    @property
    def headers(self):
        return [ f['name'] for f in self.schema['fields'] ]

    def rows(self, keyed=False):
        if keyed:
            return [ dict(self.headers, row) for row in self.buffer_ ]
        else:
            return self.buffer_

    def buffer(self):
        return self.buffer_

    def __str__(self):
        if isinstance(self.buffer_, list):
            data = '\n'.join([ str(x) for x in self.buffer_[:2] ])
            return '%s\n%s' % (self.schema, data)
        else:
            return 'Stream %s' % self.buffer_


def runFlowSychronous(config, steps, debug=True):
    reader = steps[0]
    processors = steps[1:-1]
    writer = steps[-1]
    print('Running ... %s' % reader.__name__)
    resource = DataResource(reader(config['source']))
    for step in processors:
        print('Running ... %s' % step.__name__)
        print(resource)
        resource = DataResource(step(resource))

    print('Running ... %s' % writer.__name__)
    print(resource)
    writer(resource) 

