def serializeCgiToServer(coors):
    string = ""
    for i in range(0, len(coors)):
        string += str(coors[i][0]) + "," + str(coors[i][1])
        string += ";"
    return string.encode('utf-8')
    
def deserializeCgiToServer(string):
    string = string.decode('utf-8')
    
    splitted = string.split(";")
    coors = [None]*(len(splitted)-1)
    for i in range(0,len(splitted)-1):
        coors[i] = splitted[i].split(",")
    return coors

def serializeServerToCgi(distanceMatrix):
    string = ""
    for i in range(0, len(distanceMatrix)):
        for j in range(0, len(distanceMatrix[i])):
            string += str(distanceMatrix[i][j]) + ","
        string += ";"
    return string.encode('utf-8')
    
def deserializeServerToCgi(string):
    string = string.decode('utf-8')
    
    splitted = string.split(";")
    distanceMatrix = [None]*(len(splitted)-1)
    for i in range(0,len(splitted)-1):
        row = splitted[i].split(",")
        distanceMatrix[i] = row[0:len(row)-1]
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