class VirtualObject:
    """
    VirtualObject is for objects that don't have any data but shouldn't raise any error when calling.
    """
    def __init__(self):
        pass

    def __getattribute__(self, item):
        """
        Emulates any parameter
        :param item: attribute name
        :return: magic method if magic method else self
        """
        if item[0:2] == "__" and item[-1] == "_" and item[-2] == "_":
            return super(VirtualObject, self).__getattribute__(item)
        else:
            return self

    def __setattr__(self, key, value):
        """
        Does nothing
        :param key: string - name of attribute
        :param value: any - attribute value
        :return: None
        """
        pass

    def __call__(self, *args, **kwargs):
        """
        Returns self
        :param args: anything
        :param kwargs: anything
        :return: self
        """
        return self
