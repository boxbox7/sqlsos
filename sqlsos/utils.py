def get_class_fields(cls):
    for t in dir(cls):
        if not t.startswith('__'):
            yield t
