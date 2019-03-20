import string, math,random

def distancesFromCoords():
    f = open('kroA100.tsp')
    data = [line.replace("\n","").split(" ")[1:] for line in f.readlines()[6:106]]
    coords =  list(map(lambda x: [float(x[0]),float(x[1])], data))
    distances = []
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append(math.sqrt((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2))
        distances.append(row)
    return distances

def calculateZ(myList,distances): 
    sum=0
    for i in range(len(myList)-2):
        fromCity=myList[i] #el numero en la posicion i. (que puede ser del 0 al 99)
        toCity=myList[i+1]
        sum=sum+distances[fromCity][toCity]
    return sum

def generateInitialSolution(nCities):
    list1=[i for i in range(nCities)]
    list2=[]
    while len(list1)>0:
        rand1=random.randint(0,len(list1)-1)
        list2.append(list1.pop(rand1))
    list2.append(list2[0])
    return list2

def disturbSolution(citiesList):
    disturb=citiesList[:]
    rand1=random.randint(0,99)
    rand2=random.randint(0,99)
    temp1=disturb[rand1]
    disturb[rand1]=disturb[rand2]
    disturb[rand2]=temp1
    disturb[len(disturb)-1]=disturb[0]
    return disturb

def matrizHeuristicaLocal(matrizDistancias):
    #first we make a safe copy
    matrizHL=matrizDistancias[:]
    for i in range(len(matrizDistancias)):
        for j in range(len(matrizDistancias[i])):
            matrizHL[i][j]=1/matrizHL[i][j]
    return matrizHL

def ZeroMatrizOfSameDimension(matrizGuia):
    nrow=len(matrizGuia)
    ncol=len(matrizGuia[0])
    matriz=[]
    for i in range(nrow):
        row=[]
        for j in range(ncol):
            row.append(0)
        matriz.append(row)
    return matriz



def explo_matrizFeromonaInicial(matrizDistancias,n):
    #Creamos matriz inicialziada en 0 de ncities x ncities
    matrizFeromonas=ZeroMatrizOfSameDimension(matrizDistancias)
    #Generamos cualquier solucion inicial
    nSolution=generateInitialSolution(len(matrizDistancias))
    #el ciclo se repetira n veces primero (100 esta bien)
    while(n>0):
        #en cada iteracion se probara con una solucion aleatoria y apartir de su Z
        #se llenara la matriz de feromonas
        nSolution=disturbSolution(nSolution)
        zOfCurrentSolution=calculateZ(nSolution,matrizDistancias)
        inverseZ=1/zOfCurrentSolution
        #-2 porque la ultima ciudad(len -1 ) no ira a ninguna, ya sera la primera desde donde se partio
        for i in range(len(nSolution)-2):
            fromCity=nSolution[i]
            toCity=nSolution[i+1]
            matrizFeromonas[fromCity][toCity]+=inverseZ
            
        #al final de la iteracion n.i generamos otra solucion para que la matriz de feromonas
        #se actualice con respecto a otra nueva solucion     
        n-=1
    return matrizFeromonas


if __name__ == "__main__":
    lista=generateInitialSolution(2)
    matrix= distancesFromCoords()
    matrixFeromonas=explo_matrizFeromonaInicial(matrix,1000)

    print(matrixFeromonas)



