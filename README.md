# Argument Agent Communication Model

This repository contains a Python implementation of a communication model based on argumentation between agents. The model is implemented using the Mesa framework, which provides an agent-based modeling toolkit in Python.

## Requirements
The following packages are required to run the model:
* mesa
To install it, run 
```
pip install mesa
```

## Usage
The communication model can be run by executing the `main.py` script:
```
python main.py
```

## Model Description
The model is based on the concept of argumentation between agents to reach an agreement on a preferred item. Each agent has a list of items and an associated preference order based on several criteria. The agents communicate with each other by exchanging messages containing proposals, arguments, and acceptances.

The model consists of the following classes (only the main classes are listed):

* `ArgumentAgent`: Represents an agent in the model. Each agent has a preference order and a list of items. The agent communicates with other agents by sending and receiving messages.

* `Message`: Represents a message sent between agents. The message contains the sender, performative, and content.

* `MessagePerformative`: An enumeration that represents the different types of performative that can be used in a message, including propose, accept, argue, and ask why.

* `Preferences`: Represents the preferences of an agent. Each agent has its own order of importance for criteria, and has its own beliefs on each item's value for each criterium.

* `Item`: Represents an item in the model.

* `Argument`: Represents an argument for a particular item.

## Implementation details
The model only runs with two agents. One agent will propose its preferred item. \
If the proposed item is also the most preferred item of the other agent, they will agree on this item.\
If the proposed item is among the top 10% items of the other agent, it will propose its own preferred item.\
Else the other agent will ask why the first one proposed this item.\

If an agent receives an 'ask why', it will give a weak argument supporting its preferred item to leave room for debate.\
If an agent receives an argument it will try to counter it.\
As soon as an agent doesn'gt find any counter argument, it will accept the item of the other agent.\

The agents will never repeat an argument.
