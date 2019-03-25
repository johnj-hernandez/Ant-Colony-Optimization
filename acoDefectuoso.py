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

#calcula el costo de la lista de ciudades la cual incluye las 100 ciudades + la inicial
#RECIBE: numero lista de ciudades o solucion y matriz de adjacencia
#RETORNA un valor numerico con el valor de z
def calculateZ(myList,distances): 
    sum=0
    for i in range(len(myList)-1): #se detiene en -2 para llegar a la penultima ciudad porque la ultima es el retorno
        fromCity=myList[i] #el numero en la posicion i. (que puede ser del 0 al 99)
        toCity=myList[i+1]
        sum=sum+distances[fromCity][toCity]
    return sum

#Genera una solucion con 100 ciudades + la inicial como ultima
def generateInitialSolution(nCities):
    list1=[i for i in range(nCities)]
    list2=[]
    while len(list1)>0:
        rand1=random.randint(0,len(list1)-1)
        list2.append(list1.pop(rand1))
    list2.append(list2[0])
    return list2

# def disturbSolution(citiesList):
#     disturb=citiesList[:]
#     rand1=random.randint(0,99)
#     rand2=random.randint(0,99)
#     temp1=disturb[rand1]
#     disturb[rand1]=disturb[rand2]
#     disturb[rand2]=temp1
#     disturb[len(disturb)-1]=disturb[0]
#     return disturb

#retorna una matriz igual que la de adjacencia pero con los valores 1/x
def matrizHeuristicaLocal(matrizDistancias):
    #first we make a safe copy
    matrizHL=matrizDistancias[:]
    for i in range(len(matrizDistancias)):
        for j in range(len(matrizDistancias[i])):
            if(matrizHL[i][j] !=0 ):
                matrizHL[i][j]=1/matrizHL[i][j]
    return matrizHL

#metodo manual para hacer una matriz en 0 de las mismas dimenciones de la matriz pasada
#usada para crear la matriz de feromonas inicial
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


def isNotAdded(lista,valor):
    flat=True
    for i in lista:
        if i ==valor:
            return False
    return flat




def explo_matrizFeromonaInicial(matrizDistancias,n):
    #Creamos matriz inicialziada en 0 de ncities x ncities
    matrizFeromonas=ZeroMatrizOfSameDimension(matrizDistancias)
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



############# incompleto#############################################################
#se debe verificar que el total de j con los que se trabaja en ambas ocasiones es el mismo
#se estan repitiendo algunos valores
def calcularj(i,alfa,beta,listaActual,matFeromona,matHerustica):
    nCiudades=len(matFeromona)
    ran=random.random()
    sumaProbabilidades=0
    j=0
    sumDenominador=0
        # primero encontramos la suma de todas las probabilidades
    for j in range(nCiudades):
        if isNotAdded(listaActual,j): 
            prob=(matFeromona[i][j]**alfa)*(matHerustica[i][j]**beta)
            #print(prob)
            sumDenominador+=prob
            #print(sumDenominador)
        #ahora que tenemos el denominador ahora si procedemos a ir sumando las 
        #probabilidades de las ciudades hasta que sea superior a el numero aleatorio
    j=0
    while ran>sumaProbabilidades:
        if isNotAdded(listaActual,j): 
            prob= ((matFeromona[i][j]**alfa)*(matHerustica[i][j]**beta))/sumDenominador
            print(i,j,prob,sumaProbabilidades,ran)
            sumaProbabilidades+=prob
        if(j==99):
            break
        j+=1
    return j

#suponiendo que el metodo de encontrar j esta bien, me dira a donde debo moverme dado un i
def AntColony(distances):
    nCiudades=len(distances)
    matFeromonas=explo_matrizFeromonaInicial(distances,1000)
    matHeuristica=matrizHeuristicaLocal(distances)
    #A partir  de aqui se crearan los 100 ciudades iniciado y terminando en la ciudad 0 
    solucion=[0]
    current=0
    for i in range(nCiudades-1):
        current=calcularj(current,1,1,solucion,matFeromonas,matHeuristica)
        #print(current)
        solucion.append(current)
    solucion.append(solucion[0])
    # una vez tengamos la solucion vamos a llenar la feromona 
    zOfCurrentSolution=calculateZ(solucion,distances)
    inverseZ=1/zOfCurrentSolution
    #-2 porque la ultima ciudad(len -1 ) no ira a ninguna, ya sera la primera desde donde se partio
    for i in range(nCiudades-1):
        fromCity=solucion[i]
        toCity=solucion[i+1]
        matFeromonas[fromCity][toCity]+=inverseZ
    print(solucion)
            

###############################################################################
def evaporacion(solucionAceptada,matrizFeromonas,ro):
    #para las 100 ciudades o trancisiones
    for i in range(len(solucionAceptada)-2):
        fromcity=solucionAceptada[i]
        toCity=solucionAceptada[i+1]
        for j in range(len(solucionAceptada)-2):
            if(j!=toCity):
                matrizFeromonas[fromcity][j]*=(1-ro)






if __name__ == "__main__":
    matrix= distancesFromCoords()
    AntColony(matrix)



