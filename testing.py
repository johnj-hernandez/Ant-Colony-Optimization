lista=[[1,2],[3]]
def matrizHeuristicaLocal(matrizDistancias):
    #first we make a safe copy
    matrizHL=matrizDistancias[:]
    for i in range(len(matrizDistancias)):
        for j in range(len(matrizDistancias[i])):
            matrizHL[i][j]=1/matrizHL[i][j]
    return matrizHL
print(matrizHeuristicaLocal(lista))
