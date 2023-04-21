# Argument Agent Communication Model

This repository contains a Python implementation of a communication model based on argumentation between agents. The model is implemented using the Mesa framework, which provides an agent-based modeling toolkit in Python.

## Requirements
The following packages are required to run the model:
* mesa

## Installation
To install the dependencies, run:
```
pip install -r requirements.txt
```

## Usage
The communication model can be run by executing the `run_model.py` script:
```
python run_model.py
```

## Model Description
The model is based on the concept of argumentation between agents to reach an agreement on a preferred item. Each agent has a list of items and an associated preference order based on several criteria. The agents communicate with each other by exchanging messages containing proposals, arguments, and acceptances.

The model consists of the following classes:

* `ArgumentAgent`: Represents an agent in the model. Each agent has a preference order and a list of items. The agent communicates with other agents by sending and receiving messages.

* `Message`: Represents a message sent between agents. The message contains the sender, receiver, performative, and content.

* `MessagePerformative`: An enumeration that represents the different types of performative that can be used in a message, including propose, accept, argue, and ask why.

* `Preferences`: Represents the preference order of an agent. The preference order is based on several criteria, including price, quality, and popularity.

* `CriterionValue`: Represents the value of a criterion for a particular item.

* `CriterionName`: An enumeration that represents the different criteria that can be used in the preference order.

* `Value`: An enumeration that represents the different values that can be assigned to a criterion.

* `Item`: Represents an item in the model.

* `Argument`: Represents an argument for a particular item.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
