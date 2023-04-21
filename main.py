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
        self.generate_preferences(item_list)    #Les préférences (ordre d'importance des critères et les opinions sur les items) sont générées aléatoirement
        self.item_list = item_list

        self.preferred_item_name = self.pref.most_preferred(self.item_list).get_name()
        self.agreed = False

        self.arguments_used = []    #On utilise pas les mêmes arguments en boucle
        self.other_agent_preferred_item_name = None #utile pour accepter l'item de l'autre

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

        #Si on nous propose un item
        if perf == MessagePerformative.PROPOSE:
            self.other_agent_preferred_item_name = content

            #Si l'item proposé dans le top 10, on propose le notre (et on accepte si c'est le meme)
            if self.pref.is_item_among_top_10_percent(self.get_item_from_name(content), self.item_list):
                if content == self.preferred_item_name:
                    self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ACCEPT, self.preferred_item_name))
                else:
                    self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.PROPOSE, self.preferred_item_name))
            else:   #Sinon on demande pourquoi cet item
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ASK_WHY, content)) 
        
        elif perf == MessagePerformative.ASK_WHY:   #Si on recoit un pourquoi, on donne l'argument le plus faible en faveur de notre item (pour laisser place au débat)
            argument = self.support_proposal(self.preferred_item_name)
            self.arguments_used.append(argument) 
            if argument is not None:
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ARGUE, argument))  
            else:
                #On accepte notre défaite à la première demande d'argument, ne devrait pas arriver
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ACCEPT, "J'accepte, j'ai absolument aucun argument pour mon item preferré"))

        elif perf == MessagePerformative.ARGUE: #Si on recoit un argument on tente de le contrer
            if self.other_agent_preferred_item_name is None and content.item != self.preferred_item_name:   #Si c'est la première fois que l'autre propose son item, on mémorise son nom
                self.other_agent_preferred_item_name = content.item

            arg = None
            for potential_arg in self.find_counter_args(content):
                if potential_arg not in self.arguments_used:
                    arg = potential_arg
                    self.arguments_used.append(potential_arg)
                    break

            
            if arg is None: #Si on ne peut pas contrer l'argument de l'autre, on accepte son item
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ACCEPT, self.other_agent_preferred_item_name))
            else:
                self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.ARGUE, arg))
        
        elif perf == MessagePerformative.ACCEPT and content == self.preferred_item_name:
            self.agreed = True
            self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.COMMIT, self.preferred_item_name))        
        elif perf == MessagePerformative.COMMIT:
            #Si on en recoit un ca veut dire qu'on a accepté avant
            self.agreed = True
            self.send_message(Message(self.get_name(), interlocuteur, MessagePerformative.COMMIT, content))   
        
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

    def get_item_from_name(self, name):
        for item in self.item_list:
            if item.get_name() == name:
                return item
            
    def support_proposal(self, item):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        param item : str - name of the item which was proposed
        return : string - the weakest supportive argument -> LEAVE ROOM FOR DEBATING
        """
        arg =  Argument(True, item)
        premiss = arg.list_supporting_proposal(self.get_item_from_name(item), self.pref)[-1]
        arg.couple_values_list.append(premiss)
        return arg

    def counter_crit(self, debated_crit, debated_item):
        #On va parcourir la liste de nos critères plus importants que celui avancé
        #On va chercher si parmis eux, un critère a une mauvaise valeur pour l'item débattu si ce n'est pas le notre
        #Sinon on va chercher si on a une bonne valeur pour l'item qu'on propose
        res = []
        for crit_name in self.pref.get_criterion_name_list():
            if crit_name == debated_crit:
                break
            if debated_item.get_name() != self.preferred_item_name:   #Si on contre un argument qui propose un objet qui n'est pas le notre
                if self.pref.get_value(self.get_item_from_name(self.preferred_item_name), crit_name).value > 2:
                    new_arg = Argument(True, self.preferred_item_name)
                    new_arg.add_premiss_comparison(crit_name, debated_crit)
                    new_arg.add_premiss_couple_values(crit_name, self.pref.get_value(self.get_item_from_name(self.preferred_item_name), crit_name))
                    res.append(new_arg)
            else:   #Si l'item avancé n'est pas le notre et qu'on a une mauvaise valeur sur le critère annoncé 
                if self.pref.get_value(debated_item, crit_name).value < 2:
                    new_arg = Argument(False, debated_item.get_name())
                    new_arg.add_premiss_comparison(crit_name, debated_crit)
                    new_arg.add_premiss_couple_values(crit_name, self.pref.get_value(debated_item, crit_name))
                    res.append(new_arg)
        return res

    def find_counter_args(self, argument): 
        #print(f"Trying to counter {argument}")
        counter_args = [] 
        debated_item = self.get_item_from_name(argument.item)

        #print(self.pref.get_criterion_name_list())

        # On attaque sur le critère
        for comp in argument.comparison_list:
            counter_args.extend(self.counter_crit(comp.best_criterion_name, debated_item))

        
        for couple in argument.couple_values_list:
            #print(self.pref.get_value(debated_item, couple.criterion_name))

            # On attaque sur le critère
            counter_args.extend(self.counter_crit(couple.criterion_name, debated_item))

            #Si notre item préféré a une meilleure valeur sur un critère énoncé que celui proposé
            if couple.value.value < self.pref.get_value(self.get_item_from_name(self.preferred_item_name), couple.criterion_name).value:
                new_arg = Argument(not argument.boolean_decision, debated_item.get_name())
                new_arg.add_premiss_couple_values(couple.criterion_name, self.pref.get_value(debated_item, couple.criterion_name))
                counter_args.append(new_arg)

        return counter_args



class SpeakingModel(Model):
    """ """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)


        item_list = [Item(f"Engine {i}", f"{i}") for i in range(20)]

        A1 = ArgumentAgent(0, self, "Alice", item_list)
        A2 = ArgumentAgent(1, self, "Bob", item_list)
        self.schedule.add(A1)
        self.schedule.add(A2)
        
        A1.send_message(Message(A1.get_name(), "Bob", MessagePerformative.PROPOSE, A1.preferred_item_name))

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
    
    def finished_debating(self):
        for agent in self.schedule.agents:
            if not agent.agreed:
                return False
            
        return True



if __name__ == "__main__":
    # Init the model and the agents
    speaking_model = SpeakingModel()
    MessageService.get_instance().set_instant_delivery(False)

    while not speaking_model.finished_debating():
        speaking_model.step()
