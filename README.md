# CISC/CMPE 204 Modelling Project

The Game of Life is a discrete model of computation and was invented by British mathematician John Horton Conway, 
and was popularized in 1970. It is a cellular automaton that is played on an infinitely-sized grid. 
The game is self-operating; a “zero player game” where once the initial conditions are set, 
the game plays itself. Each cell can take on one of two states— it can either be alive, or it can be dead. 
Then, in each new stage, the game plays itself and cells either die, revive, 
continue surviving, or remain dead based on the above conditions.

Our project aims to determine if any given state is a stable state. 
We will logically determine if any current sequence of cells is a stable state. 
Specifically, our model will correspond to the positions of cells that are alive and make up a stable state. 
The outcome will provide us with all the models that are stable states (depending on our configurations), 
and output a sample solution.

## Structure


* `documents`: Contains all the files for the draft and final submissions. 
* `visualizer.py`: Helper python file in order to create a visual representation in the terminal. 
* `currentRun.py`: Main running function, contains all the propositions and constraints. 
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
* `Dockerfile`: Unedited Dockerfile used to create the Docker Image. 


