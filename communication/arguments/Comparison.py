class Comparison:
    """Comparison class.
    This class implements a comparison object used in argument object.
    attr:
        best_criterion_name
        worst_criterion_name
    """

    def __init__(self, best_criterion_name, worst_criterion_name):
        self.best_criterion_name=best_criterion_name
        self.worst_criterion_name=worst_criterion_name

    def toString(self):
        return f"{self.best_criterion_name} > {self.worst_criterion_name}"
    
    def __eq__(self, other):
        return (self.best_criterion_name, self.worst_criterion_name) == (other.best_criterion_name, other.worst_criterion_name)