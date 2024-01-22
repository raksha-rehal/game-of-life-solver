
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from visualizer import create_visualization

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

E = Encoding()

#Here is where we put the specifications for the model, 
#Height and width are the details for the size of the grid. 
#gameLength is the amount of turns  we want to grid to be stable by, must be >0
#For example, a gameLength of 1 would mean the state is stable within 1 turn, 
height = 4
width = 4
gameLength = 4
Propositions = []
constraintType = "normal" #normal, reverse, atLeast1, totalSolutions in order for which rules to use. 

#Create nested list to hold the propositions, 
for i in range(gameLength+1):
    Propositions.append([])
    for w in range(width):
        Propositions[i].append([])


@proposition(E)
class AliveProposition:
    def __init__(self, height, width, time):
        self.row = width
        self.col = height
        self.time = time
    def __repr__(self):
        return f"A({self.time},{self.row},{self.col})"


#Create the propositions for ecah round and place them in the correct spot in the nested list. 
for l in range(gameLength+1):
    for w in range(width):
        for h in range(height):    
            Propositions[l][w].append(AliveProposition(h,w,l))

#Create the neighbour value, A value to alwyas represent false 
#when a proposition is bordering the edge of the grid
Invalid = AliveProposition("Invalid","Invalid","Invalid")

#Function that creates a statement of conjunts and disjunts representing the proposition,
#Where there are 3 alive neighbours surrounding the parameter
#parameters 
#   pProp - AliveProposition - The space that we want to check. 
#returns
#   Boolean Equation representing the statement, 
def findNeighbours3(pProp):
    w = pProp.row
    h = pProp.col
    t = pProp.time
    
    if w == 0:
        n1 = Invalid
    else:
        n1 = Propositions[t][w-1][h]
    if h == 0:
        n2 = Invalid
    else:
        n2 = Propositions[t][w][h-1]
        
    if w == width-1:
        n3 = Invalid
    else:
        n3 = Propositions[t][w+1][h]

    if h == height-1:
        n4 = Invalid
    else:
        n4 = Propositions[t][w][h+1]

    return ((~n1 & n2 & n3 & n4) | (n1 & ~n2 & n3 & n4) | (n1 & n2 & ~n3 & n4) | (n1 & n2 & n3 & ~n4))

#Function that creates a statement of conjunts and disjunts representing the proposition,
#Where there are 2 or 3 alive neighbours surrounding the parameter
#parameters 
#   pProp - AliveProposition - The space that we want to check. 
#returns
#   Boolean Equation representing the statement, 
def findNeighbours2V3(pProp):
    w = pProp.row
    h = pProp.col
    t = pProp.time
    #Set each of the neighoburs to a variable, then create the long string of conjuncts and disjuncts. 
    if w == 0:
        n1 = Invalid
    else:
        n1 = Propositions[t][w-1][h]
    if h == 0:
        n2 = Invalid
    else:
        n2 = Propositions[t][w][h-1]
    if w == width-1:
        n3 = Invalid
    else:
        n3 = Propositions[t][w+1][h]
    if h == height-1:
        n4 = Invalid
    else:
        n4 = Propositions[t][w][h+1]
    # The comment out return statement is an alternate equivalent version of the current version we used for testing, 
    # It is equal to ~(0,1, or 4 neibhours), this should be equivalent to (2 or 3 neighbours)  
    # return ~((~n1 & ~n2 & ~n3 & ~n4) | (n1 & ~n2 & ~n3 & ~n4) | (~n1 & n2 & ~n3 & ~n4) | (~n1 & ~n2 & n3 & ~n4) | (~n1 & ~n2 & ~n3 & n4) | (n1 & n2 & n3 & n4))
    return  (n1 & n2 & ~n3 & ~n4)|(n1 & ~n2 & n3 & ~n4)|(n1 & ~n2 & ~n3 & n4)| (~n1 & n2 & ~n3 & n4)|(~n1 & n2 & n3 & ~n4)|(n1 & n2 & ~n3 & ~n4)| (~n1 & ~n2 & n3 & n4)|(~n1 & n2 & n3 & ~n4)|(n1 & ~n2 & n3 & ~n4)| (~n1 & ~n2 & n3 & n4)|(~n1 & n2 & ~n3 & n4)|(n1 & ~n2 & ~n3 & n4)| ((~n1 & n2 & n3 & n4) | (n1 & ~n2 & n3 & n4) | (n1 & n2 & ~n3 & n4) | (n1 & n2 & n3 & ~n4))
def example_theory():   
    #The Invalid is a proposition that is always false that represents the neighbours that are out of bounds,
    E.add_constraint(~Invalid)
    
    if constraintType == "normal":
        #Iterate through each proposition in the game and define its behavour. 
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):    
                    A = Propositions[x][y][z]
                    #Constraints Defining the rules of the game
                    E.add_constraint(((~A & findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
        for q in range(width):
            for w in range(height):
                #Stable State Constraints,
                E.add_constraint(Propositions[gameLength-1][q][w]>> Propositions[gameLength][q][w])
                E.add_constraint(~Propositions[gameLength-1][q][w]>> ~Propositions[gameLength][q][w])
        return E

#   The reverse set of rules outlined in the documentation. 
    elif constraintType == "reverse":
        #Iterate through each proposition in the game and define its behavour. 
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):    
                    #Constraints Defining the rules of the game
                    A = Propositions[x][y][z]
                    E.add_constraint(((~A & findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> Propositions[x+1][y][z]))

        for q in range(width):
            for w in range(height):
                #Constraints For Stable State, 
                E.add_constraint(Propositions[gameLength-1][q][w]>> Propositions[gameLength][q][w])
                E.add_constraint(~Propositions[gameLength-1][q][w]>> ~Propositions[gameLength][q][w])
        return E

#   Same as normal rules, except with an additional condition where there has to be at 
#   least 1 alive proposition in the final grid. 
    elif constraintType == "atLeast1":
        
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):    
                    #Constraints Defining the rules of the game
                    A = Propositions[x][y][z]
                    E.add_constraint(((~A & findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
                    
        for q in range(width):
            for w in range(height):
                #Stable State Constraints
                E.add_constraint(Propositions[gameLength-1][q][w]>> Propositions[gameLength][q][w])
                E.add_constraint(~Propositions[gameLength-1][q][w]>> ~Propositions[gameLength][q][w])
        constraint.add_at_least_one(E, Propositions[gameLength-1])
        
        return E
#   A version of normal with the stable state restriction taken out. 
#   Used to find the total amonut of possible combinations for a certian grid.
    elif constraintType == "totalSolutions":
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):   
                    #Constraints Defining the rules of the game
                    A = Propositions[x][y][z]
                    E.add_constraint(((~A & findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
        return E



if __name__ == "__main__":
    T = example_theory()
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions:ls %d" % count_solutions(T))
    create_visualization(T.solve(), Propositions)

    
