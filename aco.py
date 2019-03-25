import numpy as np
import math,random
lista=[1,2,3]


def matrizHeuristicaLocal(matrizDistancias):
    #first we make a safe copy
    matrizHL=np.copy(matrizDistancias)
    for i in range(len(matrizDistancias)):
        for j in range(len(matrizDistancias[i])):
            if(matrizHL[i][j] !=0 ):
                matrizHL[i][j]=1/matrizHL[i][j]
    return matrizHL

def generateInitialSolution(nCities):
    list1=[i for i in range(nCities)]
    list2=[]
    while len(list1)>0:
        rand1=random.randint(0,len(list1)-1)
        list2.append(list1.pop(rand1))
    list2.append(list2[0])
    return list2


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
    for i in range(len(myList)-1): #se detiene en -2 para llegar a la penultima ciudad porque la ultima es el retorno
        fromCity=myList[i] #el numero en la posicion i. (que puede ser del 0 al 99)
        toCity=myList[i+1]
        sum=sum+distances[fromCity][toCity]
    return sum

def explo_matrizFeromonaInicial(matrizDistancias,n):
    #Creamos matriz inicialziada en 0 de ncities x ncities
    matrizFeromonas=np.zeros(np.shape(matrizDistancias))
    #Generamos cualquier solucion inicial
    nSolution=generateInitialSolution(len(matrizDistancias))
    #el ciclo se repetira n veces primero (1000 estaria bien)
    while(n>0):
        #en cada iteracion se probara con una solucion aleatoria y apartir de su Z
        #se llenara la matriz de feromonas
        #no es perturbar es general una matriz totalmente Distinta
        nSolution=generateInitialSolution(len(matrizDistancias))
        zOfCurrentSolution=calculateZ(nSolution,matrizDistancias)
        inverseZ=1/zOfCurrentSolution
        #-2 porque la ultima ciudad(len -1 ) no ira a ninguna, ya sera la primera desde donde se partio
        for i in range(len(nSolution)-1):
            fromCity=nSolution[i]
            toCity=nSolution[i+1]
            matrizFeromonas[fromCity][toCity]+=inverseZ
            
        #al final de la iteracion n.i generamos otra solucion para que la matriz de feromonas
        #se actualice con respecto a otra nueva solucion     
        n-=1
    return matrizFeromonas

def matrizProbabilidades(heuristica,feromona,aplha,beta,actual):
    feromona=np.array(feromona)
    heuristica=np.array(heuristica)
    #esto representa el numerador
    matriz=(feromona**aplha)*(heuristica**beta)
    #ahora hacemos el denominador que es la suma de cada columna
    for i in actual:
        matriz[i,:]=0

    #denominador
    #sumatoria=np.sum(matriz,axis=0)
    sumatoria=matriz.sum(axis=0)

    #la matriz de probabilidades
    probabilidades=matriz/sumatoria
    return probabilidades

#cuando pase por el camino se llenara la feromona y se borrara, eso va despues de usar este metodo
def generatePath(heuristica,feromona,aplha,beta):
    contador=0
    actual=[0]
    while(len(actual)<len(feromona)):
        ran=random.random()
        probabilidades=matrizProbabilidades(heuristica,feromona,aplha,beta,actual)
        actual.append(posicionAcumuladoSuperaRandom(probabilidades[:,actual[contador]],ran,actual))
        contador+=1
    actual.append(0)
    return actual
    
def agregarFeromona(feromona,nSolution,distancias):
    feromona2=np.copy(feromona)
    zOfCurrentSolution=calculateZ(nSolution,distancias)
    inverseZ=1/zOfCurrentSolution
        #-2 porque la ultima ciudad(len -1 ) no ira a ninguna, ya sera la primera desde donde se partio
    for i in range(len(nSolution)-1):
        fromCity=nSolution[i]
        toCity=nSolution[i+1]
        feromona2[fromCity][toCity]+=inverseZ
    return feromona2


def antColonyOptimization(distancias,aplha,beta,evap,iterations):
    feromona=explo_matrizFeromonaInicial(distancias,1000)
    feromona=np.array(feromona)
    heuristica=np.array(matrizHeuristicaLocal(distancias))
    for i in range(iterations):
        solucion=generatePath(heuristica,feromona,aplha,beta)
        feromona=agregarFeromona(feromona,solucion,distancias)
        feromona=feromona*(1-evap)
        print("la solucion actual es:",solucion)
        print("y su valor es: ",calculateZ(solucion,distancias))
    print(solucion)
    print("el valor de z es: ",calculateZ(solucion,distancias))





def posicionAcumuladoSuperaRandom(lista,ran,actual):
    acumulado=0
    for j in range(len(lista)):
        #que siempre calcule el acumulado y simplemente se detenga cuando lo haya excedido y no este en la actual 
        acumulado+=lista[j]
        #si no esta ya agregado
        if lista[j] in actual:
            continue
        else:
            if(acumulado>ran):
                return j
    return 0








#####MAIN##################
if __name__ == "__main__":
    antColonyOptimization(distancesFromCoords(),1,5,0.1,100)

