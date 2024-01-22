#Takes in a dictionary from the T.solve() and outputs a easier to read representation of the game
def create_visualization(Parm, pProp):
    if Parm != None:
        print("Here is an arbitrary stable state with the given configuration: ")
        for val in pProp:
            for key in val:
                for barb in key:
                    if Parm[barb]:
                        print("1", end=" ")
                    else:
                        print("0", end=" ")
                print("\n")
            print("\n\n")
    print("   Solution: %s" % Parm)
