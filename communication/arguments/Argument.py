from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue
from communication.preferences.Value import Value

class Argument:
    """ Argument class .
    This class implements an argument used during the interaction .

    attr :
        decision
        item
        comparison_list
        couple_values_list
    """
    

    def __init__(self, boolean_decision, item):
        self.boolean_decision = boolean_decision
        self.item = item
        self.comparison_list = []
        self.couple_values_list = []

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list."""
        pass

    def add_premiss_couple_values(self, criterion_name, value):
        """ Add a premiss couple values in the couple values list"""
        pass

    def list_supporting_proposal(self, item, preferences):
        """ Generate a list of premisses which can be used to support an item
        param item : Item - the item
        return : list of all premisses PRO an item ( sorted by order of importance based on agent's preferences )
        """

        res = []
        for crit_name in preferences.get_criterion_name_list():
            val = preferences.get_value(item, crit_name)
            if val == Value.VERY_GOOD or val == Value.GOOD:
                res.append(f"{item} <- {crit_name} = {val}")
        return res
                


    def list_attacking_proposal(self, item, preferences):
        """ Generate a list of premisses which can be used to attack an item
            param item : Item - name of the item
            return : list of all premisses CON an item ( sorted by order of importance based on preferences )
        """
        res = []
        for crit_name in preferences.get_criterion_name_list():
            val = preferences.get_value(item, crit_name)
            if val == Value.VERY_BAD or val == Value.BAD:
                res.append(f"{item.get_name()} <- {crit_name} = {val}")
        return res

