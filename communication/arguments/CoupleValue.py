class CoupleValue:
    """ CoupleValue class.
    This class implements a couple value used in argument object.

    attr:
        criterion_name
        value
    """

    def __init__(self, criterion_name, value):
        self.criterion_name=criterion_name
        self.value=value

    def toString(self):
        return f"{self.criterion_name} = {self.value}"
    
    def __eq__(self, other):
        return (self.criterion_name, self.value) == (other.criterion_name, other.value)
