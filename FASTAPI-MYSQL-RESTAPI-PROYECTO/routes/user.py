import re
import csv 
import json
import pandas as pd
import numpy as np
from fastapi import APIRouter, Response
from config.db import conn
from models.user import consultas
from schemas.user import User,Usuario, Centro_costo, Cargo, Contrato, Candidato, Personal, Experiencia_laboral, Consulta
from logic import logic
from cryptography.fernet import Fernet
from starlette import status
from sqlalchemy.sql import select

key = Fernet.generate_key()
f = Fernet(key)
user = APIRouter()

@user.get("/consultaDinamica/{varConsul}-{varOrd}", tags=["consulta"])
async def get_TablasDinamicas(varConsul : str, varOrd : str ):
    sql="SELECT * FROM "+varConsul
    sql2=" WHERE "
    print(sql)    
    return conn.execute(sql+";").fetchall()  
    #return None  

@user.get("/consultaJaccard/{varConsul}", tags=["consulta"])
async def get_TablasConsultaJaccard(varConsul : str): 
    url = 'https://raw.githubusercontent.com/impostorkemar/ProyectoML/main/Proyecto.csv'
    archivo = pd.read_csv(url,sep=',')
    dEtnica=[]; dXenofobia=[]; dLGBTI=[]; dGenero=[]; dRacial=[]; 

    for i in range(len(archivo)):
        dEtnica.append(archivo.iloc[i]['Discriminación étnica y racial'])
        dXenofobia.append(archivo.iloc[i]['Discriminación contra personas extranjeras o xenofobia'])
        dLGBTI.append(archivo.iloc[i]['Discriminación contra las personas lesbianas-gays-bisexuales-transgénero e intersexuales (LGBTI)'])
        dGenero.append(archivo.iloc[i]['Discriminación de género'])   
        dRacial.append(archivo.iloc[i]['Discriminación por discapacidad']) 
    sql= str(varConsul)   
    print("\nSQL\n",sql)        
    tit = []
    tit.append(sql)   
    #print("\nTIT:\n",tit)
    df = pd.DataFrame(tit)    
    #print("DF:",df)
    #NLP    
    dEtnica = logic.cleanList(dEtnica,"es")
    dXenofobia = logic.cleanList(dXenofobia,"es")
    dLGBTI = logic.cleanList(dLGBTI,"es")
    dGenero = logic.cleanList(dGenero,"es")
    dRacial = logic.cleanList(dRacial,"es")
    #Creando colección
    TitleColection = logic.cleanColection(tit,"es")   
    
    TitleColection.append(dEtnica)
    TitleColection.append(dXenofobia)
    TitleColection.append(dLGBTI)
    TitleColection.append(dGenero)
    TitleColection.append(dRacial)
    print("\nTitleColection:\n",TitleColection)
    #Creando vocabulario (full inverted index)
    Vocabulary = logic.create_Vocabulary(TitleColection)  
    #print("\nVocabulary:\n",Vocabulary)  
    Ocurrencys = logic.create_Ocurrencys(Vocabulary,TitleColection) 
    logic.print_Dictionary(Vocabulary,Ocurrencys)
      
    #JACCARD (TITLE y KEYWORD)
    TitleJaccard = logic.matrizJaccard(TitleColection)
    TitleJaccard = pd.DataFrame(TitleJaccard, columns = ['Consulta','dEtnica','dXenofobia','dLGBTI','dGenero','dRacial'])
    print("\nJaccard:\n",TitleJaccard)        
    dfJson1=TitleJaccard.to_json(orient="records")
    parsed = json.loads(dfJson1)
    json.dumps(parsed, indent=4)
    print(parsed)
    return parsed

@user.get("/consultaCoseno/{varConsul}", tags=["consulta"])
async def get_TablasConsultaCoseno(varConsul : str): 
    url = 'https://raw.githubusercontent.com/impostorkemar/ProyectoML/main/Proyecto.csv'
    archivo = pd.read_csv(url,sep=',')
    dEtnica=[]; dXenofobia=[]; dLGBTI=[]; dGenero=[]; dRacial=[];

    for i in range(len(archivo)):
        dEtnica.append(archivo.iloc[i]['Discriminación étnica y racial'])
        dXenofobia.append(archivo.iloc[i]['Discriminación contra personas extranjeras o xenofobia'])
        dLGBTI.append(archivo.iloc[i]['Discriminación contra las personas lesbianas-gays-bisexuales-transgénero e intersexuales (LGBTI)'])
        dGenero.append(archivo.iloc[i]['Discriminación de género'])    
        dRacial.append(archivo.iloc[i]['Discriminación por discapacidad'])
    sql= str(varConsul)   
    print("\nSQL\n",sql)        
    tit = []
    tit.append(sql)   
    #print("\nTIT:\n",tit)
    df = pd.DataFrame(tit)    
    #print("DF:",df)
    #NLP    
    dEtnica = logic.cleanList(dEtnica,"es")
    dXenofobia = logic.cleanList(dXenofobia,"es")
    dLGBTI = logic.cleanList(dLGBTI,"es")
    dGenero = logic.cleanList(dGenero,"es")
    dRacial = logic.cleanList(dRacial,"es")
    TitleColection = logic.cleanColection(tit,"es")   
    #Creando colección
    TitleColection.append(dEtnica)
    TitleColection.append(dXenofobia)
    TitleColection.append(dLGBTI)
    TitleColection.append(dGenero)
    TitleColection.append(dRacial)
    print("\nTitleColection:\n",TitleColection)
    #Creando vocabulario (full inverted index)
    Vocabulary = logic.create_Vocabulary(TitleColection)  
    #print("\nVocabulary:\n",Vocabulary)  
    Ocurrencys = logic.create_Ocurrencys(Vocabulary,TitleColection) 
    logic.print_Dictionary(Vocabulary,Ocurrencys)
      
    #Calculos para COSENO    
    MatrizTF_Abstratc = logic.create_MatrizTF(Ocurrencys,len(TitleColection))
    #print("\nMatriz TF\t\t","Tamaño:",MatrizTF_Abstratc.shape,"\n", MatrizTF_Abstratc) #Impresión bolsa de palabras
    MatrizWTF_Abstratc = logic.create_MatrizWTF(MatrizTF_Abstratc)
    #print("\nMatriz WTF\t\t","Tamaño:",MatrizWTF_Abstratc.shape,"\n", MatrizWTF_Abstratc) #Impresión Matriz WTF
    MatrizDF_Abstratc = logic.crear_MatrizDF(MatrizWTF_Abstratc)
    #print("\nMatriz DF\t\t","Tamaño:",MatrizDF_Abstratc.shape,"\n", MatrizDF_Abstratc) #Impresión Matriz DF
    MatrizIDF_Abstratc = logic.crear_MatrizIDF(MatrizDF_Abstratc,len(TitleColection))
    #print("\nMatriz IDF\t\t","Tamaño:",MatrizIDF_Abstratc.shape,"\n", MatrizIDF_Abstratc) #Impresión Matriz IDF
    MatrizTF_IDF_Abstratc = logic.crear_MatrizTF_IDF(MatrizWTF_Abstratc,MatrizIDF_Abstratc)
    #print("\nMatriz TF_IDF\t\t","Tamaño:",MatrizTF_IDF_Abstratc.shape,"\n", MatrizTF_IDF_Abstratc) #Impresión Matriz TF_IDF
    nColumnas = np.shape(MatrizWTF_Abstratc)[1];
    matrizNorma = logic.create_mCoseNorm(nColumnas,MatrizTF_IDF_Abstratc)
    print("\nMatriz TF_IDF NORM\t\t","Tamaño:",matrizNorma.shape,"\n", matrizNorma) #Impresión Matriz TF_IDF
    matrizCoseno = logic.create_mCose(nColumnas,matrizNorma)
    #print("\nMatriz Distancia Abstracts \t\t","Tamaño:",matrizCoseno.shape,"\n", matrizCoseno) #Impresión Matriz TF_IDF
    #Archivo importados
    df2 = pd.DataFrame(matrizCoseno, columns = ['Consulta','dEtnica','dXenofobia','dLGBTI','dGenero','dRacial'])
    print("COSENO:\n",df2)
    dfJson2=df2.to_json(orient="records")
    parsed = json.loads(dfJson2)
    json.dumps(parsed, indent=4)
    print(parsed)
    return parsed

@user.get("/consultaNTokens/{varConsul}", tags=["consulta"])
async def get_TablasConsultaNTokens(varConsul : str): 
    url = 'https://raw.githubusercontent.com/impostorkemar/ProyectoML/main/Proyecto.csv'
    archivo = pd.read_csv(url,sep=',')
    dEtnica=[]; dXenofobia=[]; dLGBTI=[]; dGenero=[]; dRacial=[];

    for i in range(len(archivo)):
        dEtnica.append(archivo.iloc[i]['Discriminación étnica y racial'])
        dXenofobia.append(archivo.iloc[i]['Discriminación contra personas extranjeras o xenofobia'])
        dLGBTI.append(archivo.iloc[i]['Discriminación contra las personas lesbianas-gays-bisexuales-transgénero e intersexuales (LGBTI)'])
        dGenero.append(archivo.iloc[i]['Discriminación de género'])  
        dRacial.append(archivo.iloc[i]['Discriminación por discapacidad'])  
    sql= str(varConsul)   
    #print("\nSQL\n",sql)        
    tit = []
    tit.append(sql)   
    #print("\nTIT:\n",tit)
    df = pd.DataFrame(tit)    
    #print("DF:",df)
    #NLP    
    dEtnica = logic.cleanList(dEtnica,"es")
    dXenofobia = logic.cleanList(dXenofobia,"es")
    dLGBTI = logic.cleanList(dLGBTI,"es")
    dGenero = logic.cleanList(dGenero,"es")
    dRacial = logic.cleanList(dRacial,"es")
    TitleColection = logic.cleanColection(tit,"es")  
    #Calculo de numero de tokens
    contadorD,totalW=logic.PorcentajeTRokens(sql,dEtnica,dXenofobia,dLGBTI,dGenero,dRacial) 
    print("len",contadorD,"TIT:\n",tit)    
    porcentaje=[round(contadorD/totalW,2)]
    #porcentaje=len(TitleColection)/contadorD    
    df2 = pd.DataFrame(porcentaje, columns = ['Respuesta'])
    print("RESPONSE:\n",df2)
    dfJson2=df2.to_json(orient="records")
    parsed = json.loads(dfJson2)
    json.dumps(parsed, indent=4)
    print(parsed)
    return parsed
    
