# Makes it so a list is full of None values.
def Nonefy(size):
    list = [None] * size
    return list

def swap_bool(boolean):
    print(boolean)
    if boolean == True:
        boolean = False
        print("true")
    else:
        boolean = True
        print("false")
    print(boolean)
    return boolean
    