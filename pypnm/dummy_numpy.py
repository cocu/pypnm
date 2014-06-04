class DummyNumpy(object):
    @classmethod
    def empty(cls, data_type):
        if len(data_type) == 0:
            return 0
        return [cls.empty(data_type[:-1])for _ in range(data_type[-1])]
    
    @classmethod
    def array(cls, l):
        return l
