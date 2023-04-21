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
    
    def __repr__(self):
        s = "-" if not self.boolean_decision else ""
        s += f"{self.item} <- "
        
        for premiss in self.comparison_list+self.couple_values_list:
            s+= premiss.toString() + ', '

        return s[:-2] #on vire le dernier ', '
        
    def __eq__(self, other):
        #on va juste comparer les premiss comme on argumente juste entre deux items
        for comp in self.comparison_list:
            if comp not in other.comparison_list:
                return False
        for couple in self.couple_values_list:
            if couple not in other.couple_values_list:
                return False
        
        for comp in other.comparison_list:
            if comp not in self.comparison_list:
                return False
        for couple in other.couple_values_list:
            if couple not in self.couple_values_list:
                return False
        return True


    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list."""
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """ Add a premiss couple values in the couple values list"""
        self.couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposal(self, item, preferences):
        """ Generate a list of premisses which can be used to support an item
        param item : Item - the item
        return : list of all premisses PRO an item ( sorted by order of importance based on agent's preferences )
        """

        res = []
        for crit_name in preferences.get_criterion_name_list():
            val = preferences.get_value(item, crit_name)
            if val == Value.VERY_GOOD or val == Value.GOOD:
                res.append(CoupleValue(crit_name, val))
        return res

    def list_attacking_proposal(self, item, preferences):
        """ Generate a list of premisses which can be used to attack an item
            param item : Item - name of the item
            return : list of all premisses CON an item ( sorted by order of importance based on preferences )
        """
        # We will not use this function due to implementation choices

        res = []
        for crit_name in preferences.get_criterion_name_list():
            val = preferences.get_value(item, crit_name)
            if val == Value.VERY_BAD or val == Value.BAD:
                res.append(CoupleValue(crit_name, val))
        return res

