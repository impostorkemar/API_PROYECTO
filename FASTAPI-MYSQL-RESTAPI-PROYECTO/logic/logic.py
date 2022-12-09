import re
import pandas as pd
import numpy as np
import urllib.request
import io
import math
import nltk
from bs4 import BeautifulSoup
from  urllib.request import urlopen 
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from unicodedata import normalize
def remove_values_from_list(the_list, val):
    for i in range(the_list.count(val)):
        the_list.remove(val)

def cleanList (cole,language):    
    colecciontok=[]; colection_v2 = []; stemmer = PorterStemmer(); 
    if language == "es":
      lng = "spanish"
    elif language == "en":
      lng = "english"  
    else:
      lng = "spanish"
    n = stopwords.words(lng)#lista de stopwords    
    documentoaux = np.array(cole, dtype=str)
    for i in cole: # Dar formato sin eliminar stopwords xq pierdo semántica
      documentoaux = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", i), 0, re.I)
      #print("documentoaux1:",documentoaux)
      documentoaux2 = re.sub('[^A-Za-z0-9áéíóú[ñ]]+','',documentoaux)
      #print("documentoaux2:",documentoaux2)
      documentoaux = documentoaux2.lower()# poner todo en minúsculas  
      #print("documentoaux:",documentoaux)
      k=0 
      colection_v2.append(stemmer.stem(documentoaux))    #insertar en lista colection_v2 
    return colection_v2

def cleanColection(colection,language):
  colection_v2 = [];  stemmer = PorterStemmer(); 
  if language == "es":
    lng = "spanish"
  elif language == "en":
    lng = "english"  
  else:
    lng = "spanish"
  #print(n[n.index('es')])
  n = stopwords.words(lng)#lista de stopwords
  #print("n-->",n)
  for i in colection: # Dar formato sin eliminar stopwords xq pierdo semántica
    i_format = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", i), 0, re.I)
    #print("format1:",i_format)
    i_format2 = re.sub('[^A-Za-z0-9áéíóúñ]+',' ',i_format)
    #print("\tformat2:",i_format2)
    i_lower = i_format2.lower()  #hacer minúsculas
    #print("\t\tlower:",i_lower)
    i_splited = i_lower.split() #hacer spliteo
    #print("\t\tsplited:",i_splited, len(i_splited))   
    k=0
    i_splited2 = []
    for word in i_splited:      
      #print("tamSpli",len(i_splited),"Element",i_splited[k])
      if n.count(i_splited[k]) == 0:
        #print("NO EXISTE")
        i_splited2.append(i_splited[k])
        #print("\t\tSinStopwords:",i_splited2, len(i_splited2))
      #else:
        #print("EXISTE")        
      k += 1  
    i_stem = []  
    for token in i_splited2:   #Stemming  
      i_stem.append(stemmer.stem(token))
    colection_v2.append(i_stem)    #insertar en lista colection_v2    
  return colection_v2

def create_Vocabulary(colection):
  Matriz = []
  for list in colection:    #Crear vocabulario con Tokens
    for word in list:
      if  word not in Matriz:      
        Matriz.append(word) 
  Vocabulary = np.array(Matriz, dtype=object)
  return Matriz

def create_Dictionary(Vocabulary,colection_v2):  
  matriz = []
  for i in range(len(Vocabulary)): #Crear Diccionario vacío
      matriz.append([])
  #Crear Diccionario con ocurrencias 
  for i in range(len(Vocabulary)):   #Recorrer vocabulario
    for j in range(len(colection_v2)):  #Recorrer Colección seteada con formato
      aux=[]; indices = []; k=0;       
      for word in colection_v2[j]:  #Recorrer palabras de cada lista en Colección
        if Vocabulary[i] == colection_v2[j][k]: #Encontrando palabra
          indices.append(k+1)  
        k += 1
      if len(indices) > 0:  
        aux.extend([j+1,len(indices),indices])        
        matriz[i].append(aux)        
  Diccionary = np.array(matriz) 
  return Diccionary

#Obtiene posición en la tabla hash según la hashfunction
def hash_Function(dividendo, divisor):
    return dividendo % divisor
#Obtiene el valor de K para una estrategia de redispersión
def k_Value(x, B):
    return hash_Function(x, B - 1) + 1
#Nueva posición en la tabla hash según calculo de K
def rehashing_Function(hPos, k, B):
    return hash_Function(hPos + k, B)
#Imprimir hash table
def print_HashTable(hashTable):
    for i in range(len(hashTable)):
        print(i, ' | ', hashTable[i])
#Calcular factor de carga
def charge_Factor(nElementos, tamTablaHash):
    return nElementos / tamTablaHash
#Imprimir detalle de factor de carga
def print_chargeFactor(hashTable):
    nNone = 0;
    for i in range(len(hashTable)):
        if (hashTable[i] is None):
            nNone += 1
    nElementosRegis = len(hashTable) - nNone
    print('Factor de Carga Real: ', charge_Factor(nElementosRegis, len(hashTable)), ' \nElementos:', nElementosRegis,
          '\tCubetas:', len(hashTable))
#Permitir valores B solo primos
def is_Prime(n):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True
# Calcular tamaño de hash table mediante el número de elementos llenados en la tabla / la longitud de la tabla hash
def tam_TablaHash_X_ChargeFactor(elementos, factorCargaIdeal):
    tamTablaHash = int(round(len(elementos) / factorCargaIdeal, 0))
    while is_Prime(tamTablaHash) == 0: #B debe ser primo
        tamTablaHash += 1
        # print(tamTablaHash, isPrime(tamTablaHash))
    else:
        return tamTablaHash

def create_Ocurrencys(Vocabulary,colection_v2):  
  matriz = []
  for i in range(len(Vocabulary)): #Crear Diccionario vacío
      matriz.append([])
  #Crear Diccionario con ocurrencias 
  for i in range(len(Vocabulary)):   #Recorrer vocabulario
    for j in range(len(colection_v2)):  #Recorrer Colección seteada con formato
      aux=[]; indices = []; k=0;       
      for word in colection_v2[j]:  #Recorrer palabras de cada lista en Colección
        if Vocabulary[i] == colection_v2[j][k]: #Encontrando palabra
          indices.append(k+1)  
        k += 1
      if len(indices) > 0:  
        aux.extend([j+1,len(indices),indices])        
        matriz[i].append(aux)        
  Ocurrency = np.array(matriz, dtype=object) 
  return Ocurrency
  
def print_Dictionary(Vocabulary,dictionary):  
  print("Vocabulario\tOcurrencias")
  for i in range(len(dictionary)):
    print(f"{i+1} => {Vocabulary[i]:8}\t-->{dictionary[i]}")

def matrizJaccard(coleccion):
    matriz = np.zeros((len(coleccion),len(coleccion)))
    i = j = 0
    while True:
        if matriz[i][j] == 0:
            matriz[i][j] = matriz[j][i] = jaccard(coleccion[i],coleccion[j])
        j += 1
        if j == len(coleccion):
            j = 0 
            i += 1
        if i == len(coleccion):
            break
    return matriz

def create_MatrizTF(dictionary,lenColection):
  auxMFrecuency = np.zeros([len( dictionary),lenColection], dtype=float)
  print("Tamaño matriz incidenica: M",np.shape(auxMFrecuency)) # tamaño matriz bolsa de palabras
  #print(auxMFrecuency)
  i=0; j=0
  for filas in dictionary:
    matriz = []
    for elemento in filas:
      #print("[i,j]=[",i,",",j,"] =", elemento[0]," ",elemento[1])
      auxMFrecuency[i][elemento[0]-1] = elemento[1]
      j += 1
    i += 1
    #print(matriz)
    #print("\n")    
  return auxMFrecuency;

def create_MatrizWTF(Matriz):
  Matriz2 = Matriz;   i=0;   nFilas = np.shape(Matriz2)[0];   nColumnas = np.shape(Matriz2)[1];
  #print("filas:",nFilas,"columnas:",nColumnas) 
  for fila in Matriz:  
    cont=0
    for j in range(len(fila)):
      #print(Matriz[i][j])        
      if (Matriz[i][j] == 0):
        Matriz2[i][j] = 0
      else:
        Matriz2[i][j] = 1 + np.log10(Matriz[i][j])     
        cont += 1         
    i += 1 
  return Matriz2

def crear_MatrizDF(MatrizWTF):
  frecuency = []
  for lista in MatrizWTF:
    frecuency.append(np.count_nonzero(lista))
  DF = np.array(frecuency, dtype=object)
  return DF

def crear_MatrizIDF(MatrizDF,tamanoN):
  frecuencyNormalized = []
  for item in MatrizDF:
    frecuencyNormalized.append(math.log10(tamanoN/item))
  IDF = np.array(frecuencyNormalized, dtype=object)
  return IDF

def crear_MatrizTF_IDF(MatrizWTF,MatrizIDF):  
  i =0;  j = 0; matriz = np.zeros((len(MatrizWTF),len(MatrizWTF[0])));

  for lista in MatrizWTF:
    for j in range(0,len(lista)):
      matriz[i][j] = MatrizWTF[i][j]*MatrizIDF[i]
    i +=1
  TF_IDF = np.array(matriz, dtype=object)
  return TF_IDF

def create_mCoseNorm(nColumnas,Matriz):  
  for i in range(nColumnas):
    #print("columna",i,":", Matriz[:,i]**2)
    modulo = np.sqrt(np.sum(Matriz[:,i]**2))
    #print("module:",round(modulo,2))
    Matriz[:,i] = Matriz[:,i]/modulo
  return Matriz

def  create_mCose(nColumnas,Matriz): 
  mCose = np.zeros([nColumnas, nColumnas], dtype=object)#declarar matriz de cos  
  j = 0
  for i in range(0,mCose.shape[0]):
    for j in range(0,mCose.shape[1]):
      if i == j:
        mCose[i][j] = 1
      elif i < j:     
        #print(sum(Matriz[:,i]*Matriz[:,j]))
        mCose[i][j] = sum(Matriz[:,i]*Matriz[:,j])
  return mCose

def matrizDistPonderada(matriz1,matriz2,matriz3,ponderacines):
    matrizDistancias = np.zeros((len(matriz1),len(matriz1)))
    i = j = 0
    while True:
        matrizDistancias[i][j] = matriz1[i][j]*ponderacines[0] + matriz2[i][j]*ponderacines[1] + matriz3[i][j]*ponderacines[2]
        j += 1
        if j ==  len(matriz1):
            j = 0
            i += 1
        if i == len(matriz1):
            break
    return matrizDistancias
##Jaccardd
def interseccion(a,b):
    cont=0
    for token in a:
        if token in b:
            cont += 1
    return cont

def union(a,b):
    uni = []
    for token in a:
        if token not in uni:
            uni.append(token)
    for token in b:
        if token not in uni:
            uni.append(token)
    #print(uni)
    return len(uni)

def jaccard(a,b):
    intersec = interseccion(a,b)  
    uni = union(a,b) 
    return round(intersec/uni,2)
def to_ascii(text):
    ascii_values = [ord(character) for character in text]
    return ascii_values

def PorcentajeTRokens(tit,dEtnica,dXenofobia,dLGBTI,dGenero,dRacial):
  print("TIT:",tit)
  tokens=tit.split()
  print(tit.split())  
  print("Tokens:",tokens)
  tokens = cleanList(tokens,"es")
  cont=0  
  print("DTEST:",dLGBTI)  
  for word in tokens:      
    if word in dEtnica: 
      #print("TRUE")      
      cont += 1
    elif word in dXenofobia:  
      #print("TRUE")       
      cont += 1
    elif word in dLGBTI:     
      #print("TRUE")    
      cont += 1
    elif word in dGenero:
      #print("TRUE") 
      cont += 1
    elif word in dRacial:
      #print("TRUE") 
      cont += 1
    else:
      cont += 0
    print("word:",word, "cont:",cont,"len:", len(tokens)) 
  return cont,len(tokens)
