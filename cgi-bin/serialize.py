def serializeCgiToServer(coors): #coors is a n by 2 2D array of doubles
    string = ""
    for i in range(0, len(coors)):
        string += str(coors[i][0]) + "," + str(coors[i][1]) # add comma between x and y coor
        string += ";" # add semicolon to seperate coors
    string += "\n" #ending character
    return string.encode('utf-8')
    
def deserializeCgiToServer(string):
    string = string.decode('utf-8')
    
    splitted = string.split(";")
    coors = [None]*(len(splitted)-1) # create list: [None, None, None,...] with length len(splitted)-1
    for i in range(0,len(splitted)-1):
        coors[i] = splitted[i].split(",")
        coors[i] = [float(x) for x in coors[i]] # convert to float
    return coors

def serializeServerToCgi(distanceMatrix): # distanceMatrix is matrix of doubles
    string = ""
    for i in range(0, len(distanceMatrix)):
        for j in range(0, len(distanceMatrix[i])):
            string += str(distanceMatrix[i][j]) + "," # seperate distances with comma
        string += ";" # seperate rows with semicolon
    string += "\n" # ending character
    return string.encode('utf-8')
    
def deserializeServerToCgi(string):
    string = string.decode('utf-8')
    
    splitted = string.split(";")
    distanceMatrix = [None]*(len(splitted)-1)
    for i in range(0,len(splitted)-1):
        row = splitted[i].split(",")
        distanceMatrix[i] = row[0:len(row)-1]
        distanceMatrix[i] = [float(x) for x in distanceMatrix[i]] # convert to float
    return distanceMatrix
    
def testFunctions():
    string = serializeCgiToServer([[1,2]])
    coors = deserializeCgiToServer(string)
    print(coors)
    string = serializeServerToCgi([[10,6,5]])
    distanceMatrix = deserializeServerToCgi(string)
    print(distanceMatrix)



#if __name__ == '__main__':
#    testFunctions()