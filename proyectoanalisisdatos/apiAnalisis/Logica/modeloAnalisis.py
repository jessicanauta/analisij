from django.db import models
from django.urls import reverse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
import seaborn as sns
from sklearn import preprocessing
from apiAnalisis import models
import os
import pathlib

class modeloAnalisis():
    """Clase modelo Analisis"""
    dfOriginal=pd.DataFrame([])
    DataframeTransformado1=pd.DataFrame([])
    def suma(num1=0,num2=0):
        resultado=num1+num2
        return resultado

    def predecirTipoCliente(self,Dni=0):
        print('Dni:',Dni)
        self.preprocesamiento(self)
        tipoCliente, edad=self.predecir(self,Dni)
        #print(tipoCliente)
        if tipoCliente==1:
            mensaje='Dni:',Dni,', es un buen cliente.'
            dbReg=models.Cliente(cedula=Dni, edad=edad, tipoCliente=tipoCliente)
            dbReg.save()
        elif tipoCliente==2:
            mensaje='Dni:',Dni,', es un mal cliente'
            dbReg=models.Cliente(cedula=Dni, edad=edad, tipoCliente=tipoCliente)
            dbReg.save()
        else:
            mensaje='No existe el cliente con Dni:',Dni
        return mensaje

    def predecir(self,Dni=0):
        cliente=self.dfOriginal.loc[self.dfOriginal['DNI'] == Dni]
        #print('cliente: ',cliente)
        edad=cliente['EDAD'].values
        edad=edad[0]
        tipoCliente=2
        if not(cliente.empty):
            print('Existe el cliente')
            indiceCliente=cliente.index.values[0]
            print('Indice: ',indiceCliente)
            cliente=self.DataframeTransformado1.loc[ indiceCliente , : ]
            historialCredito=round(cliente[0],2)
            saldoAhorros=round(cliente[1],2)
            tiempoEmpleo=round(cliente[2],2)
            activos=round(cliente[4],2)
            print('Historial de Crédito:', historialCredito, ' Saldo:',saldoAhorros, ' Tiempo de empleo:', tiempoEmpleo, ' Activos:',activos, ' Edad:',edad)
            if activos<0.5 and edad>25 and (historialCredito<0.5 or saldoAhorros>0.5 or tiempoEmpleo>0.5):
                tipoCliente=1
            else:
                tipoCliente=2
        else:
            tipoCliente=3
        return tipoCliente, edad

    def preprocesamiento(self):
        self.dfOriginal = pd.read_csv('apiAnalisis/Datasets/DatasetBanco/3.DatasetBanco.csv', sep=";")
        dataframe=self.dfOriginal
        #print(dataframe.shape)
        salida = self.dfOriginal.TIPOCLIENTE.values
        dataframe=dataframe.drop(['DNI'], axis=1)
        dataframe=dataframe.drop(['TIPOCLIENTE'], axis=1)
        #print(dataframe.shape)

        categorical_ordinal = ['HISTORIALCREDITO','SALDOCUENTAAHORROS','TIEMPOEMPLEO','ESTADOCIVILYSEXO','ACTIVOS','VIVIENDA','EMPLEO']
        categorical_nominal = ['PROPOSITOCREDITO','GARANTE','TRABAJADOREXTRANJERO']
        numerical = ['PLAZOMESESCREDITO','MONTOCREDITO','TASAPAGO','AVALUOVIVIENDA','EDAD','CANTIDADCREDITOSEXISTENTES']
        preprocesador1 = make_column_transformer(
            (OrdinalEncoder(),categorical_ordinal),
            (OneHotEncoder(sparse=False),categorical_nominal),
            remainder='passthrough'
            )

        X = preprocesador1.fit_transform(dataframe)
        #print(X.shape[1])
        #print(X.shape)

        np.set_printoptions(formatter={'float': lambda X: "{0:0.0f}".format(X)})
        #print(preprocesador1)
        cnamesDataset1 = categorical_ordinal
        cnamesDataset2 = preprocesador1.transformers_[1][1].get_feature_names(categorical_nominal)
        cnamesDataset3 = numerical
        cnamesDataset1.extend(cnamesDataset2)
        cnamesDataset1.extend(cnamesDataset3)
        #print(cnamesDataset1)

        DataframePreprocesado = pd.DataFrame(data=X,columns=cnamesDataset1)
        DataframePreprocesado = pd.concat([DataframePreprocesado, self.dfOriginal[['TIPOCLIENTE']]], axis = 1)
        DataframePreprocesado.to_csv("apiAnalisis/Datasets/DatasetBanco/4.DatasetBancoPreprocesado.csv", sep=";",index = False) #sep es el separador, por defector es ","
        
        cr=DataframePreprocesado.corr()
        cr=round(cr,3)
        #print(cr)

        # Min max scaling
        DataframePreprocesado=DataframePreprocesado.drop(['TIPOCLIENTE'], axis=1)
        data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
        data_scaled_minmax = data_scaler_minmax.fit_transform(DataframePreprocesado)
        #print("\nDatos normalizados con escala Min Max:\n", data_scaled_minmax)

        self.DataframeTransformado1 = pd.DataFrame(data=data_scaled_minmax,columns=cnamesDataset1)
        self.DataframeTransformado1 = pd.concat([self.DataframeTransformado1, self.dfOriginal[['TIPOCLIENTE']]], axis = 1)
        self.DataframeTransformado1.to_csv("apiAnalisis/Datasets/DatasetBanco/5.DatasetBancoTransformadoMinMax.csv", sep=";",index = False) #sep es el separado, por defector es ","
        return "listo"

