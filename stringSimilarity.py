import numpy as np


def initialMatrix():

    stringOne = input("Enter first string: ")
    stringTwo = input("Enter second string: ")

    strOneLen = len(stringOne)
    strTwoLen = len(stringTwo)

    if(strOneLen == 0 or strTwoLen == 0): 
        return 0

    dimensions = (strOneLen+1, strTwoLen+1)
    matrix = np.zeros(dimensions)
    
    for i in range(0, strTwoLen+1):
        matrix[0][i] = i
    
    for i in range(0, strOneLen+1):
        matrix[i][0] = i

    return dlDistance(stringOne, stringTwo, matrix)

def dlDistance(s1, s2, matrix):

    if(len(s1) == 0 and len(s2)>0):
        print("String difference: " + str(len(s1)))
        return "String difference: " + str(len(s2))
    
    if(len(s2) == 0 and len(s1)>0):
        print("String difference: " + str(len(s1)))
        return "String difference: " + str(len(s1))

    for j in range(1, len(s1)+1):
        for i in range(1, len(s2)+1):

            if(s1[j-1] == s2[i-1]):
                matrix[j][i] = matrix[j-1][i-1]
            else:
                minimum = min(matrix[j-1][i-1], matrix[j-1][i], matrix[j][i-1], matrix[j-2][i-2])
                matrix[j][i] = 1+minimum
    
    return str(matrix[len(s1)][len(s2)])

distance = initialMatrix()
if(distance == 0):
    print("Strings are the same")
else:
    print("String difference: " + str(distance))