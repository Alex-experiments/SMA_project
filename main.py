#!/usr/bin/env python3

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.Value import Value
from communication.preferences.Item import Item
from communication.arguments.Argument import Argument

class ArgumentAgent(CommunicatingAgent):
    """ """
    def __init__(self, unique_id, model, name, item_list):
        super().__init__(unique_id, model, name)
        self.pref = Preferences()
        self.set_criterion_order()
        self.generate_preferences(item_list)
        self.item_list = item_list

        self.preferred_item = self.pref.most_preferred(self.item_list).get_name()
        self.agreed = False

    def step(self):
        super().step()

        new_msg = self.get_new_messages()
        if len(new_msg) == 0:
            return
        
        #Dans notre modèle on ne devrait jamais recevoir plus d'un message à la fois
        assert len(new_msg) == 1  
        msg = new_msg[0]
        print(msg)

        if self.agreed:
            return

        interlocuteur = msg.get_exp()
        perf = msg.get_performative()
        content = msg.get_content()

        if perf == MessagePerformative.PROPOSE:
            if self.pref.is_item_among_top_10_percent(self.get_item_from_name(content), self.item_list):
                if content == self.preferred_item:
                    self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ACCEPT, self.preferred_item))
                else:
                    self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.PROPOSE, self.preferred_item))
            else:
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ASK_WHY, content)) 
        
        elif perf == MessagePerformative.ASK_WHY:
            argument = self.support_proposal(self.preferred_item)
            if argument is not None:
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ARGUE, argument))  
            else:
                ###On propose un autre item: il faut le choisir
                pass

        elif perf == MessagePerformative.ARGUE:
            pass
        
        
        elif perf == MessagePerformative.ACCEPT and content == self.preferred_item or perf == MessagePerformative.COMMIT and content == self.preferred_item:
            self.agreed = True
            self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.COMMIT, self.preferred_item))        
        
        
    def get_item_from_name(self, name):
        for item in self.item_list:
            if item.get_name() == name:
                return item
        
    def set_criterion_order(self):
        order = [name for name in CriterionName]
        self.model.random.shuffle(order)
        self.pref.set_criterion_name_list(order)
    
    def generate_preferences(self, item_list):
        for item in item_list:
            for criterion in self.pref.get_criterion_name_list():
                self.pref.add_criterion_value(self.generate_random_crit_value(item, criterion))

    def generate_random_crit_value(self, item, criterion):
        val = self.model.random.sample([v for v in Value], 1)[0]
        return CriterionValue(item, criterion, val)

    
    def support_proposal(self, item):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        param item : str - name of the item which was proposed
        return : string - the strongest supportive argument
        """

        # To be completed
        arg =  Argument(None, None)
        return arg.list_supporting_proposal(self.get_item_from_name(item), self.pref)[0]
    
    def argument_parsing(self, argument):
        """ returns ....
        param argument :
        return :
        """
        # To be completed

        


class SpeakingModel(Model):
    """ """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        item_list=[
            Item("Diesel Engine", "A super cool diesel engine"),
            Item("Electric Engine", "A very quiet engine"),
            Item("Oui Engine", "A"),
            Item("Non Engine", "B"),
            Item("Voila Engine", "C"),
            Item("Cependant Engine", "D"),
            Item("En effet Engine", "E"),
            Item("T'es qui Engine", "F"),
            Item("Balek Engine", "G"),
            Item("Bavzieh Engine", "H"),
            Item("Menfin Engine", "I"),
            Item("J Engine", "J"),
            Item("K Engine", "K"),
            Item("L Engine", "L"),
            Item("M Engine", "M"),
            Item("N Engine", "N"),
            Item("O Engine", "O"),
            Item("P Engine", "P"),
            Item("Q Engine", "Q"),
            Item("R Engine", "R"),
        ]

        A1 = ArgumentAgent(0, self, "Alice", item_list)
        A2 = ArgumentAgent(1, self, "Bob", item_list)
        self.schedule.add(A1)
        self.schedule.add(A2)
        
        A1.send_message(Message(A1.get_name(), "Bob", MessagePerformative.PROPOSE, A1.preferred_item))

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()



if __name__ == "__main__":
    # Init the model and the agents
    speaking_model = SpeakingModel()
    MessageService.get_instance().set_instant_delivery(False)

    step = 0
    while step < 10:
        speaking_model.step()
        step += 1
