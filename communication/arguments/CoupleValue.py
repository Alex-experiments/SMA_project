class CoupleValue:
    """ CoupleValue class.
    This class implements a couple value used in argument object.

    attr:
        #item (rajouté)
        criterion_name
        value
    """

    def __init__(self, item, criterion_name, value):
        self.item=item
        self.criterion_name=criterion_name
        self.value=value

    def __repr__(self):
        return f"{self.item} <- {self.criterion_name} = {self.value}"
