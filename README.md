# RL

## modules

### Agnt.py
The Agent uses [Sequence.py](https://github.com/myhamidi/RL/blob/master/Sequence.py), [States.py](https://github.com/myhamidi/RL/blob/master/States.py), [QModel.py](https://github.com/myhamidi/RL/blob/master/QModel.py) (wich uses [NN.py](https://github.com/myhamidi/RL/blob/master/NN.py)) and [Constraints.py](https://github.com/myhamidi/RL/blob/master/Constraints.py)

Initialize the Agent with an actionlist that can be input to the environment and a featurelist that represents the state space of the environment. By default, the last feature of the state representation must be set to "terminal", which is represented by 0 (non-terminal) or 1(terminal state).
Example 1:
```
Agt = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
```
Example 2 (Grid World):
```
Agt= Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
```

The Agent can interact with any environment that provides its current state as list and has an input interface for actions. The Agent perceives the current Environment state via ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) ``clsAgent.PerceiveEnv(state,reward)`` and provides the next action to the Environment via ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) ``clsAgent.NextAction():``.
Example:
```
Agt = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
Env = EnvGrid.clsEnvironment(10, 10, -1)
for _ in range(100):
    Agt.PerceiveEnv(Env.State(), Env.Reward())
    Env.Step(Agt.NextAction())
```

The Agent can be run in three drifferent modes: ``Offline``,``Online``, ``Silent``.   
In ``Offline`` mode (default) the Agent will store the Agents perceived states and rewards and applied actions in a sequence list, but it will not do any learning or training and act randomly (epsilon = 0) or according to a fixed Q-value based policy (epilon = 1), based on the internal Q-Table or Q-Model.  
In ``Online`` mode the Agent will store the states, rewards and actions as in ``Offline`` mode and apply a Bellman Update of the last step taken, thus updating the Q-value table continously.
In ``Silent`` mode the Agent will not store date and not do any learning. This mode is meant for already trained Agents.

The Agent has a Q-Table and a Q Model (that tries to approixmates that table) per default. The training of the Q-table happens automatically in ``Online``-Mode. Q Model Training needs to be activated via  ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) ``clsAgent.Agt.QModel.SetUp()``. Now the Q Model can be trained via ``Agt.QModel.Train(FromSequence, Bellman_Iterations=1, StopAt=[1.0e-03,0])``. 
- ``FromSequence``: The Sequence the QModel shall take a sample from and learn.  
- ``Bellman_Iterations``: Number of Bellman Updates.
- ``StopAt``: QModel fitting (via tensorflow.keras) stops when loss threshold has been reached. Per default 100 tries. Example:
```
Agt = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
Env = EnvGrid.clsEnvironment(10, 10, -1)
Agt.QModel.SetUp()
Agt.QModel.batch = 50
for _ in range(100):
    Agt.PerceiveEnv(Env.State(), Env.Reward())
    Agt.QModel.Train(Agt.Sequence)
    Env.Step(Agt.NextAction())
```

