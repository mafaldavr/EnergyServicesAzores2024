#BIBLIOTECAS NECESSÁRIAS
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import pickle
import os
from sklearn import  metrics
import numpy as np
import geopandas as gpd
import json
    
#-------------------------------------

#COEFICIENTES QUE TRADUZEM A EMISSÃO EM KW PARA GRAMAS DE CO2
fueloleo = 600.0
gasoleo = 500.0
hidrica = 0.0
geotermica = 199.0
eolica = 0.0
fotovoltaica = 0.0
residuos = 752.0
outras = 0.0
    
#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS ANTES DE MARÇO DE 2024
total = pd.read_csv('dados.csv') #ler o ficheiro
total['Data'] = pd.to_datetime(total['Ano'].astype(str) + '-' + total['Mês'].astype(str), format='%Y-%m') #criar coluna com a data
total.set_index('Data', inplace=True) #definir o índice

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DE SANTA MARIA
santa_maria_total = total[total['Ilha'] == 'Santa Maria'].copy() #dados referentes à ilha de Santa Maria
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Resíduos', 'Outras Renováveis', 'Total']
santa_maria_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
santa_maria_total['Gasóleo - CO2'] = santa_maria_total['Gasóleo'] * gasoleo #adicionar colunas com emissao de co2
santa_maria_total['Total - CO2'] = santa_maria_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DE SÃO MIGUEL
sao_miguel_total = total[total['Ilha'] == 'São Miguel'].copy() #dados referentes à ilha de São Miguel
colunas = ['Ilha', 'Resíduos', 'Total']
sao_miguel_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
sao_miguel_total['Fuelóleo - CO2'] = sao_miguel_total['Fuelóleo'] * fueloleo #adicionar colunas com emissao de co2
sao_miguel_total['Gasóleo - CO2'] = sao_miguel_total['Gasóleo'] * gasoleo
sao_miguel_total['Geotérmica - CO2'] = sao_miguel_total['Geotérmica'] * geotermica
sao_miguel_total['Total - CO2'] = sao_miguel_total['Fuelóleo - CO2'] + sao_miguel_total['Gasóleo - CO2'] + sao_miguel_total['Geotérmica - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DA TERCEIRA
terceira_total = total[total['Ilha'] == 'Terceira'].copy() #dados referentes à ilha da Terceira
colunas = ['Ilha', 'Outras Renováveis', 'Total']
terceira_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
terceira_total['Fuelóleo - CO2'] = terceira_total['Fuelóleo'] * fueloleo #adicionar colunas com emissao de co2
terceira_total['Gasóleo - CO2'] = terceira_total['Gasóleo'] * gasoleo
terceira_total['Geotérmica - CO2'] = terceira_total['Geotérmica'] * geotermica
terceira_total['Resíduos - CO2'] = terceira_total['Resíduos'] * residuos
terceira_total['Total - CO2'] = terceira_total['Fuelóleo - CO2'] + terceira_total['Gasóleo - CO2'] + terceira_total['Geotérmica - CO2'] + terceira_total['Resíduos - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DA GRACIOSA
graciosa_total = total[total['Ilha'] == 'Graciosa'].copy() #dados referentes à ilha da Graciosa
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Resíduos', 'Outras Renováveis', 'Total']
graciosa_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
graciosa_total['Gasóleo - CO2'] = graciosa_total['Gasóleo'] * gasoleo #adicionar colunas com emissao de co2
graciosa_total['Total - CO2'] = graciosa_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DE SÃO JORGE
sao_jorge_total = total[total['Ilha'] == 'São Jorge'].copy() #dados referentes à ilha de São Jorge
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_jorge_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
sao_jorge_total['Gasóleo - CO2'] = sao_jorge_total['Gasóleo'] * gasoleo #adicionar colunas com emissao de co2
sao_jorge_total['Total - CO2'] = sao_jorge_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DO PICO
pico_total = total[total['Ilha'] == 'Pico'].copy() #dados referentes à ilha do Pico
colunas = ['Ilha', 'Hídrica', 'Geotérmica', 'Resíduos', 'Outras Renováveis', 'Total']
pico_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
pico_total['Fuelóleo - CO2'] = pico_total['Fuelóleo'] * fueloleo #adicionar colunas com emissao de co2
pico_total['Gasóleo - CO2'] = pico_total['Gasóleo'] * gasoleo
pico_total['Total - CO2'] = pico_total['Fuelóleo - CO2'] + pico_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DO FAIAL
faial_total = total[total['Ilha'] == 'Faial'].copy() #dados referentes à ilha do Faial
colunas = ['Ilha', 'Geotérmica', 'Resíduos', 'Outras Renováveis', 'Total']
faial_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
faial_total['Fuelóleo - CO2'] = faial_total['Fuelóleo'] * fueloleo #adicionar colunas com emissao de co2
faial_total['Gasóleo - CO2'] = faial_total['Gasóleo'] * gasoleo
faial_total['Total - CO2'] = faial_total['Fuelóleo - CO2'] + faial_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DAS FLORES
flores_total = total[total['Ilha'] == 'Flores'].copy() #dados referentes à ilha das Flores
colunas = ['Ilha', 'Fuelóleo', 'Geotérmica', 'Resíduos', 'Outras Renováveis', 'Total']
flores_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
flores_total['Gasóleo - CO2'] = flores_total['Gasóleo'] * gasoleo #adicionar colunas com emissao de co2
flores_total['Total - CO2'] = flores_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DO CORVO
corvo_total = total[total['Ilha'] == 'Corvo'].copy() #dados referentes à ilha do Corvo
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
corvo_total.drop(columns=colunas, inplace=True) #eliminar colunas sem informação
corvo_total['Gasóleo - CO2'] = corvo_total['Gasóleo'] * gasoleo #adicionar colunas com emissao de co2
corvo_total['Total - CO2'] = corvo_total['Gasóleo - CO2']

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DE MARÇO DE 2024 (AS EMISSÕES SÃO REFERENTES AO MÊS ANTERIOR)
dados = pd.read_csv('marco.csv') #ler o ficheiro
dados['Data'] = pd.to_datetime(dados['Ano'].astype(str) + '-' + dados['Mês'].astype(str), format='%Y-%m') #criar coluna com a data
dados.set_index('Data', inplace=True) #definir o índice

#-------------------------------------

#CRIAR UMA DATAFRAME COM OS DADOS DE CADA ILHA
santa_maria = dados[dados['Ilha'] == 'Santa Maria'].copy() #dados referentes à ilha de Santa Maria
sao_miguel = dados[dados['Ilha'] == 'São Miguel'].copy() #dados referentes à ilha de São Miguel
terceira = dados[dados['Ilha'] == 'Terceira'].copy() #dados referentes à ilha da Terceira
graciosa = dados[dados['Ilha'] == 'Graciosa'].copy() #dados referentes à ilha da Graciosa
sao_jorge = dados[dados['Ilha'] == 'São Jorge'].copy() #dados referentes à ilha de São Jorge
pico = dados[dados['Ilha'] == 'Pico'].copy() #dados referentes à ilha do Pico
faial = dados[dados['Ilha'] == 'Faial'].copy() #dados referentes à ilha do Faial
flores = dados[dados['Ilha'] == 'Flores'].copy() #dados referentes à ilha das Flores
corvo = dados[dados['Ilha'] == 'Corvo'].copy() #dados referentes à ilha do Corvo

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DE SANTA MARIA
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
santa_maria_gasoleo = santa_maria.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
santa_maria_eolica = santa_maria.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
santa_maria_fotovoltaica = santa_maria.drop(columns=colunas, axis=1) #eliminar colunas sem informação
santa_maria_gasoleo_entradas = santa_maria_gasoleo.values
santa_maria_eolica_entradas = santa_maria_eolica.values
santa_maria_fotovoltaica_entradas = santa_maria_fotovoltaica.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DE SÃO MIGUEL
colunas = ['Ilha', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_miguel_fueloleo = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_miguel_gasoleo = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_miguel_hidrica = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_miguel_geotermica = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_miguel_eolica = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_miguel_fotovoltaica = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Fotovoltaica', 'Total']
sao_miguel_outras = sao_miguel.drop(columns=colunas, axis=1) #eliminar colunas sem informação
sao_miguel_fueloleo_entradas = sao_miguel_fueloleo.values
sao_miguel_gasoleo_entradas = sao_miguel_gasoleo.values
sao_miguel_hidrica_entradas = sao_miguel_hidrica.values
sao_miguel_geotermica_entradas = sao_miguel_geotermica.values
sao_miguel_eolica_entradas = sao_miguel_eolica.values
sao_miguel_fotovoltaica_entradas = sao_miguel_fotovoltaica.values
sao_miguel_outras_entradas = sao_miguel_outras.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DA TERCEIRA
colunas = ['Ilha', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
terceira_fueloleo = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
terceira_gasoleo = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
terceira_hidrica = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
terceira_geotermica = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
terceira_eolica = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
terceira_fotovoltaica = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Outras Renováveis', 'Fotovoltaica', 'Total']
terceira_residuos = terceira.drop(columns=colunas, axis=1) #eliminar colunas sem informação
terceira_fueloleo_entradas = terceira_fueloleo.values
terceira_gasoleo_entradas = terceira_gasoleo.values
terceira_hidrica_entradas = terceira_hidrica.values
terceira_geotermica_entradas = terceira_geotermica.values
terceira_eolica_entradas = terceira_eolica.values
terceira_fotovoltaica_entradas = terceira_fotovoltaica.values
terceira_residuos_entradas = terceira_residuos.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DA GRACIOSA
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
graciosa_gasoleo = graciosa.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
graciosa_eolica = graciosa.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
graciosa_fotovoltaica = graciosa.drop(columns=colunas, axis=1) #eliminar colunas sem informação
graciosa_gasoleo_entradas = graciosa_gasoleo.values
graciosa_eolica_entradas = graciosa_eolica.values
graciosa_fotovoltaica_entradas = graciosa_fotovoltaica.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DE SÃO JORGE
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_jorge_gasoleo = sao_jorge.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_jorge_eolica = sao_jorge.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
sao_jorge_fotovoltaica = sao_jorge.drop(columns=colunas, axis=1) #eliminar colunas sem informação
sao_jorge_gasoleo_entradas = sao_jorge_gasoleo.values
sao_jorge_eolica_entradas = sao_jorge_eolica.values
sao_jorge_fotovoltaica_entradas = sao_jorge_fotovoltaica.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DO PICO
colunas = ['Ilha', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
pico_fueloleo = pico.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
pico_gasoleo = pico.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
pico_eolica = pico.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
pico_fotovoltaica = pico.drop(columns=colunas, axis=1) #eliminar colunas sem informação
pico_fueloleo_entradas = pico_fueloleo.values
pico_gasoleo_entradas = pico_gasoleo.values
pico_eolica_entradas = pico_eolica.values
pico_fotovoltaica_entradas = pico_fotovoltaica.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DO FAIAL
colunas = ['Ilha', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
faial_fueloleo = faial.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
faial_gasoleo = faial.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
faial_hidrica = faial.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
faial_eolica = faial.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
faial_fotovoltaica = faial.drop(columns=colunas, axis=1) #eliminar colunas sem informação
faial_fueloleo_entradas = faial_fueloleo.values
faial_gasoleo_entradas = faial_gasoleo.values
faial_hidrica_entradas = faial_hidrica.values
faial_eolica_entradas = faial_eolica.values
faial_fotovoltaica_entradas = faial_fotovoltaica.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DAS FLORES
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
flores_gasoleo = flores.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
flores_hidrica = flores.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
flores_eolica = flores.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
flores_fotovoltaica = flores.drop(columns=colunas, axis=1) #eliminar colunas sem informação
flores_gasoleo_entradas = flores_gasoleo.values
flores_hidrica_entradas = flores_hidrica.values
flores_eolica_entradas = flores_eolica.values
flores_fotovoltaica_entradas = flores_fotovoltaica.values

#-------------------------------------

#CRIAR OS CONJUNTOS DE INPUT DO CORVO
colunas = ['Ilha', 'Fuelóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Fotovoltaica', 'Resíduos', 'Outras Renováveis', 'Total']
corvo_gasoleo = corvo.drop(columns=colunas, axis=1) #eliminar colunas sem informação
colunas = ['Ilha', 'Fuelóleo', 'Gasóleo', 'Hídrica', 'Geotérmica', 'Eólica', 'Resíduos', 'Outras Renováveis', 'Total']
corvo_fotovoltaica = corvo.drop(columns=colunas, axis=1) #eliminar colunas sem informação
corvo_gasoleo_entradas = corvo_gasoleo.values
corvo_fotovoltaica_entradas = corvo_fotovoltaica.values

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA SANTA MARIA, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('santa_maria', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
santa_maria_modelo_gasoleo = load_model('santa_maria_gasoleo.pkl')
santa_maria_previsao_gasoleo = santa_maria_modelo_gasoleo.predict(santa_maria_gasoleo_entradas) #prever a emissão elétrica
santa_maria_previsao_gasoleo_co2 = santa_maria_previsao_gasoleo * gasoleo
santa_maria_modelo_eolica = load_model('santa_maria_eolica.pkl')
santa_maria_previsao_eolica = santa_maria_modelo_eolica.predict(santa_maria_eolica_entradas) #prever a emissão elétrica
santa_maria_modelo_fotovoltaica = load_model('santa_maria_fotovoltaica.pkl')
santa_maria_previsao_fotovoltaica = santa_maria_modelo_fotovoltaica.predict(santa_maria_fotovoltaica_entradas) #prever a emissão elétrica
santa_maria_previsao = santa_maria_previsao_gasoleo_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA SÃO MIGUEL, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('sao_miguel', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
sao_miguel_modelo_fueloleo = load_model('sao_miguel_fueloleo.pkl')
sao_miguel_previsao_fueloleo = sao_miguel_modelo_fueloleo.predict(sao_miguel_fueloleo_entradas) #prever a emissão elétrica
sao_miguel_previsao_fueloleo_co2 = sao_miguel_previsao_fueloleo * fueloleo
sao_miguel_modelo_gasoleo = load_model('sao_miguel_gasoleo.pkl')
sao_miguel_previsao_gasoleo = sao_miguel_modelo_gasoleo.predict(sao_miguel_gasoleo_entradas) #prever a emissão elétrica
sao_miguel_previsao_gasoleo_co2 = sao_miguel_previsao_gasoleo * gasoleo
sao_miguel_modelo_hidrica = load_model('sao_miguel_hidrica.pkl')
sao_miguel_previsao_hidrica = sao_miguel_modelo_hidrica.predict(sao_miguel_hidrica_entradas) #prever a emissão elétrica
sao_miguel_modelo_geotermica = load_model('sao_miguel_geotermica.pkl')
sao_miguel_previsao_geotermica = sao_miguel_modelo_geotermica.predict(sao_miguel_geotermica_entradas) #prever a emissão elétrica
sao_miguel_previsao_geotermica_co2 = sao_miguel_previsao_geotermica * geotermica
sao_miguel_modelo_eolica = load_model('sao_miguel_eolica.pkl')
sao_miguel_previsao_eolica = sao_miguel_modelo_eolica.predict(sao_miguel_eolica_entradas) #prever a emissão elétrica
sao_miguel_modelo_fotovoltaica = load_model('sao_miguel_fotovoltaica.pkl')
sao_miguel_previsao_fotovoltaica = sao_miguel_modelo_fotovoltaica.predict(sao_miguel_fotovoltaica_entradas) #prever a emissão elétrica
sao_miguel_modelo_outras = load_model('sao_miguel_outras.pkl')
sao_miguel_previsao_outras = sao_miguel_modelo_outras.predict(sao_miguel_outras_entradas) #prever a emissão elétrica
sao_miguel_previsao = sao_miguel_previsao_fueloleo_co2 + sao_miguel_previsao_gasoleo_co2 + sao_miguel_previsao_geotermica_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA A TERCEIRA, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('terceira', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
terceira_modelo_fueloleo = load_model('terceira_fueloleo.pkl')
terceira_previsao_fueloleo = terceira_modelo_fueloleo.predict(terceira_fueloleo_entradas) #prever a emissão elétrica
terceira_previsao_fueloleo_co2 = terceira_previsao_fueloleo * fueloleo
terceira_modelo_gasoleo = load_model('terceira_gasoleo.pkl')
terceira_previsao_gasoleo = terceira_modelo_gasoleo.predict(terceira_gasoleo_entradas) #prever a emissão elétrica
terceira_previsao_gasoleo_co2 = terceira_previsao_gasoleo * gasoleo
terceira_modelo_hidrica = load_model('terceira_hidrica.pkl')
terceira_previsao_hidrica = terceira_modelo_hidrica.predict(terceira_hidrica_entradas) #prever a emissão elétrica
terceira_modelo_geotermica = load_model('terceira_geotermica.pkl')
terceira_previsao_geotermica = terceira_modelo_geotermica.predict(terceira_geotermica_entradas) #prever a emissão elétrica
terceira_previsao_geotermica_co2 = terceira_previsao_geotermica * geotermica
terceira_modelo_eolica = load_model('terceira_eolica.pkl')
terceira_previsao_eolica = terceira_modelo_eolica.predict(terceira_eolica_entradas) #prever a emissão elétrica
terceira_modelo_fotovoltaica = load_model('terceira_fotovoltaica.pkl')
terceira_previsao_fotovoltaica = terceira_modelo_fotovoltaica.predict(terceira_fotovoltaica_entradas) #prever a emissão elétrica
terceira_modelo_residuos = load_model('terceira_residuos.pkl')
terceira_previsao_residuos = terceira_modelo_residuos.predict(terceira_residuos_entradas) #prever a emissão elétrica
terceira_previsao_residuos_co2 = terceira_previsao_residuos * residuos
terceira_previsao = terceira_previsao_fueloleo_co2 + terceira_previsao_gasoleo_co2 + terceira_previsao_geotermica_co2 + terceira_previsao_residuos_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA A GRACIOSA, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('graciosa', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
graciosa_modelo_gasoleo = load_model('graciosa_gasoleo.pkl')
graciosa_previsao_gasoleo = graciosa_modelo_gasoleo.predict(graciosa_gasoleo_entradas) #prever a emissão elétrica
graciosa_previsao_gasoleo_co2 = graciosa_previsao_gasoleo * gasoleo
graciosa_modelo_eolica = load_model('graciosa_eolica.pkl')
graciosa_previsao_eolica = graciosa_modelo_eolica.predict(graciosa_eolica_entradas) #prever a emissão elétrica
graciosa_modelo_fotovoltaica = load_model('graciosa_fotovoltaica.pkl')
graciosa_previsao_fotovoltaica = graciosa_modelo_fotovoltaica.predict(graciosa_fotovoltaica_entradas) #prever a emissão elétrica
graciosa_previsao = graciosa_previsao_gasoleo_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA SÃO JORGE, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('sao_jorge', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
sao_jorge_modelo_gasoleo = load_model('sao_jorge_gasoleo.pkl')
sao_jorge_previsao_gasoleo = sao_jorge_modelo_gasoleo.predict(sao_jorge_gasoleo_entradas) #prever a emissão elétrica
sao_jorge_previsao_gasoleo_co2 = sao_jorge_previsao_gasoleo * gasoleo
sao_jorge_modelo_eolica = load_model('sao_jorge_eolica.pkl')
sao_jorge_previsao_eolica = sao_jorge_modelo_eolica.predict(sao_jorge_eolica_entradas) #prever a emissão elétrica
sao_jorge_modelo_fotovoltaica = load_model('sao_jorge_fotovoltaica.pkl')
sao_jorge_previsao_fotovoltaica = sao_jorge_modelo_fotovoltaica.predict(sao_jorge_fotovoltaica_entradas) #prever a emissão elétrica
sao_jorge_previsao = sao_jorge_previsao_gasoleo_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA O PICO, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('pico', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
pico_modelo_fueloleo = load_model('pico_fueloleo.pkl')
pico_previsao_fueloleo = pico_modelo_fueloleo.predict(pico_fueloleo_entradas) #prever a emissão elétrica
pico_previsao_fueloleo_co2 = pico_previsao_fueloleo *fueloleo
pico_modelo_gasoleo = load_model('pico_gasoleo.pkl')
pico_previsao_gasoleo = pico_modelo_gasoleo.predict(pico_gasoleo_entradas) #prever a emissão elétrica
pico_previsao_gasoleo_co2 = pico_previsao_gasoleo * gasoleo
pico_modelo_eolica = load_model('pico_eolica.pkl')
pico_previsao_eolica = pico_modelo_eolica.predict(pico_eolica_entradas) #prever a emissão elétrica
pico_modelo_fotovoltaica = load_model('pico_fotovoltaica.pkl')
pico_previsao_fotovoltaica = pico_modelo_fotovoltaica.predict(pico_fotovoltaica_entradas) #prever a emissão elétrica
pico_previsao = pico_previsao_fueloleo_co2 + pico_previsao_gasoleo_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA O FAIAL, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('faial', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
faial_modelo_fueloleo = load_model('faial_fueloleo.pkl')
faial_previsao_fueloleo = faial_modelo_fueloleo.predict(faial_fueloleo_entradas) #prever a emissão elétrica
faial_previsao_fueloleo_co2 = faial_previsao_fueloleo * fueloleo
faial_modelo_gasoleo = load_model('faial_gasoleo.pkl')
faial_previsao_gasoleo = faial_modelo_gasoleo.predict(faial_gasoleo_entradas) #prever a emissão elétrica
faial_previsao_gasoleo_co2 = faial_previsao_gasoleo * gasoleo
faial_modelo_hidrica = load_model('faial_hidrica.pkl')
faial_previsao_hidrica = faial_modelo_hidrica.predict(faial_hidrica_entradas) #prever a emissão elétrica
faial_modelo_eolica = load_model('faial_eolica.pkl')
faial_previsao_eolica = faial_modelo_eolica.predict(faial_eolica_entradas) #prever a emissão elétrica
faial_modelo_fotovoltaica = load_model('faial_fotovoltaica.pkl')
faial_previsao_fotovoltaica = faial_modelo_fotovoltaica.predict(faial_fotovoltaica_entradas) #prever a emissão elétrica
faial_previsao = faial_previsao_fueloleo_co2 + faial_previsao_gasoleo_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA AS FLORES, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('flores', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
flores_modelo_gasoleo = load_model('flores_gasoleo.pkl')
flores_previsao_gasoleo = flores_modelo_gasoleo.predict(flores_gasoleo_entradas) #prever a emissão elétrica
flores_previsao_gasoleo_co2 = flores_previsao_gasoleo * gasoleo
flores_modelo_hidrica = load_model('flores_hidrica.pkl')
flores_previsao_hidrica = flores_modelo_hidrica.predict(flores_hidrica_entradas) #prever a emissão elétrica
flores_modelo_eolica = load_model('flores_eolica.pkl')
flores_previsao_eolica = flores_modelo_eolica.predict(flores_eolica_entradas) #prever a emissão elétrica
flores_modelo_fotovoltaica = load_model('flores_fotovoltaica.pkl')
flores_previsao_fotovoltaica = flores_modelo_fotovoltaica.predict(flores_fotovoltaica_entradas) #prever a emissão elétrica
flores_previsao = flores_previsao_gasoleo_co2

#-------------------------------------

#FAZER LOAD DOS MÉTODOS DISPONÍVEIS PARA O CORVO, CALCULAR AS PREVISÕES E RESPETIVOS ERROS
def load_model(modelo_nome):
    modelo_caminho = os.path.join('corvo', modelo_nome)
    with open(modelo_caminho, 'rb') as ficheiro:
        modelo = pickle.load(ficheiro)
    return modelo
corvo_modelo_gasoleo = load_model('corvo_gasoleo.pkl')
corvo_previsao_gasoleo = corvo_modelo_gasoleo.predict(corvo_gasoleo_entradas) #prever a emissão elétrica
corvo_previsao_gasoleo_co2 = corvo_previsao_gasoleo * gasoleo
corvo_modelo_fotovoltaica = load_model('corvo_fotovoltaica.pkl')
corvo_previsao_fotovoltaica = corvo_modelo_fotovoltaica.predict(corvo_fotovoltaica_entradas) #prever a emissão elétrica
corvo_previsao = corvo_previsao_gasoleo_co2

#-------------------------------------

#CRIAR MAPA DOS AÇORES E ASSOCIAR A EMISSÃO TOTAL DE CO2

acores = gpd.read_file('mapa.shp') #ler o ficheiro
fig = go.Figure()
co2 = [float(santa_maria_previsao), float(sao_miguel_previsao), float(flores_previsao), float(corvo_previsao), float(graciosa_previsao), float(sao_jorge_previsao), float(faial_previsao), float(pico_previsao), float(terceira_previsao)] #criar vetor com a emissao total de co2
acores['co2'] = co2 #adicionar ao dataframe
fig.add_trace(go.Scattermapbox(
    lat=acores.centroid.y,
    lon=acores.centroid.x,
    mode='markers',
    marker=dict(size=10, color=acores['co2'], colorscale='blues', colorbar=dict(title='Emissão de CO<sub>2</sub>')),
    text=acores['Ilha'] + '<br>' + 'Emissão de CO2: ' + acores['co2'].astype(str), #mostrar nome das ilhas e emissão de co2 total
    hoverinfo='text'
))
fig.update_layout(
    mapbox=dict(
        style='carto-positron',
        center=dict(lat=38.3, lon=-28),
        zoom=6
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

#-------------------------------------

#CRIAR GRÁFICOS PARA A PREVISÃO
x = ['Santa Maria', 'São Miguel', 'Terceira', 'Graciosa', 'São Jorge', 'Pico', 'Faial', 'Flores', 'Corvo'] #eixo dos x
fig1 = go.Figure(
    data = [
        go.Bar(
        name = 'Fuelóleo',
        x = x,
        y = [0, float(sao_miguel_previsao_fueloleo), float(terceira_previsao_fueloleo), 0, 0, float(pico_previsao_fueloleo), float(faial_previsao_fueloleo), 0, 0],
        marker=dict(color='#069EE1')
                    ),
        go.Bar(
        name = 'Gasóleo',
        x = x,
        y = [float(santa_maria_previsao_gasoleo), float(sao_miguel_previsao_gasoleo), float(terceira_previsao_gasoleo), float(graciosa_previsao_gasoleo), float(sao_jorge_previsao_gasoleo), float(pico_previsao_gasoleo), float(faial_previsao_gasoleo), float(flores_previsao_gasoleo), float(corvo_previsao_gasoleo)],
        marker=dict(color='#FF8C00')
        ),
        go.Bar(
        name = 'Hídrica',
        x = x,
        y = [0, float(sao_miguel_previsao_hidrica), float(terceira_previsao_hidrica), 0, 0, 0, float(faial_previsao_hidrica), float(flores_previsao_hidrica), 0],
        marker=dict(color='#FFD700')
        ),
        go.Bar(
        name = 'Geotérmica',
        x = x,
        y = [0, float(sao_miguel_previsao_geotermica), float(terceira_previsao_geotermica), 0, 0, 0, 0, 0, 0],
        marker=dict(color='#4682B4')
        ),
        go.Bar(
        name = 'Eólica',
        x = x,
        y = [float(santa_maria_previsao_eolica), float(sao_miguel_previsao_eolica), float(terceira_previsao_eolica), float(graciosa_previsao_eolica), float(sao_jorge_previsao_eolica), float(pico_previsao_eolica), float(faial_previsao_eolica), float(flores_previsao_eolica), 0],
        marker=dict(color='#F4A460')
        ),
        go.Bar(
        name = 'Fotovoltaica',
        x = x,
        y = [float(santa_maria_previsao_fotovoltaica), float(sao_miguel_previsao_fotovoltaica), float(terceira_previsao_fotovoltaica), float(graciosa_previsao_fotovoltaica), float(sao_jorge_previsao_fotovoltaica), float(pico_previsao_fotovoltaica), float(faial_previsao_fotovoltaica), float(flores_previsao_fotovoltaica), float(corvo_previsao_fotovoltaica)],
        marker=dict(color='#FFFACD')
        ),
        go.Bar(
        name = 'Resíduos',
        x = x,
        y = [0, 0, float(terceira_previsao_residuos), 0, 0, 0, 0, 0, 0],
        marker=dict(color='#E0FFFF')
        ),
        go.Bar(
        name = 'Outras Renováveis',
        x = x,
        y = [0, float(sao_miguel_previsao_outras), 0, 0, 0, 0, 0, 0, 0],
        marker=dict(color='#FFE4B5')
        )
    ]
)
fig1.update_layout(barmode='stack')
fig1.update_xaxes(title='Ilhas')
fig1.update_yaxes(title='Produção de Eletricidade (kW)')

#-------------------------------------

#CRIAR GRÁFICOS PARA A PREVISÃO
x = ['Santa Maria', 'São Miguel', 'Terceira', 'Graciosa', 'São Jorge', 'Pico', 'Faial', 'Flores', 'Corvo'] #eixo dos x
fig2 = go.Figure(
    data = [
        go.Bar(
        name = 'Fuelóleo - CO2',
        x = x,
        y = [0, float(sao_miguel_previsao_fueloleo_co2), float(terceira_previsao_fueloleo_co2), 0, 0, float(pico_previsao_fueloleo_co2), float(faial_previsao_fueloleo_co2), 0, 0],
        marker=dict(color='#069EE1')
                    ),
        go.Bar(
        name = 'Gasóleo - CO2',
        x = x,
        y = [float(santa_maria_previsao_gasoleo_co2), float(sao_miguel_previsao_gasoleo_co2), float(terceira_previsao_gasoleo_co2), float(graciosa_previsao_gasoleo_co2), float(sao_jorge_previsao_gasoleo_co2), float(pico_previsao_gasoleo_co2), float(faial_previsao_gasoleo_co2), float(flores_previsao_gasoleo_co2), float(corvo_previsao_gasoleo_co2)],
        marker=dict(color='#FF8C00')
        ),
        go.Bar(
        name = 'Geotérmica - CO2',
        x = x,
        y = [0, float(sao_miguel_previsao_geotermica_co2), float(terceira_previsao_geotermica_co2), 0, 0, 0, 0, 0, 0],
        marker=dict(color='#FFD700')
        ),
        go.Bar(
        name = 'Resíduos - CO2',
        x = x,
        y = [0, 0, float(terceira_previsao_residuos_co2), 0, 0, 0, 0, 0, 0],
        marker=dict(color='#E0FFFF')
        )
    ]
)
fig2.update_layout(barmode='stack')
fig2.update_xaxes(title='Ilhas')
fig2.update_yaxes(title='Emissão de Co<sub>2</sub> (g)')

#-------------------------------------

#CRIAR DASHBOARD
app = dash.Dash(__name__)
app.layout = html.Div([
    
#-------------------------------------    
    
#CRIAR UM CABEÇALHO ELEGANTE
    html.H1('Emissão de Dióxido de Carbono nos Açores', style={'color':'#069EE1', 'text-align':'center', 'margin-top': '80px', 'font-family':'Arial'}), #inserir títulos
    html.H2('Serviços de Energia - Instituto Superior Técnico', style={'color':'#42545E', 'text-align':'center', 'font-family':'Arial'}),
    html.H3('Mafalda Vila Rodrigues - 100338', style={'color':'#42545E', 'text-align':'center', 'font-family':'Arial'}),
   
#-------------------------------------   
    
#CRIAR TABS COM BREVES EXPLICAÇÕES
    html.H3('Informação Útil', style={'color':'#069EE1', 'text-align':'center', 'margin-top': '80px', 'font-family':'Arial'}),
    html.Div(style={'height':'20px'}),
    dcc.Tabs([
        dcc.Tab(label='Fonte de Informação', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            html.Div(style={'height':'20px'}),
            html.H4('Os dados utilizados para calcular a emissão de diósido de Carbono no Arquipélago dos Açores são fornecidos pela Eletricidade dos Açores (EDA) e estão disponíveis ao público no seu website.', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'width': '80%', 'margin': '0 auto', 'font-family':'Arial'})
        ]),
        dcc.Tab(label='Informação Fornecida', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            html.Div(style={'height':'20px'}),
            html.H4('Este trabalho tem dois objetivos: estimar a emissão de dióxido de carbono nos últimos 5 anos e prever a emissão de dióxido de carbono no próximo mês.', style={'color':'black', 'text-align':'center', 'margin-top': '5px', 'width': '80%', 'margin': '0 auto', 'font-family':'Arial'})
        ]),
        dcc.Tab(label='Atualizações', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            html.Div(style={'height':'20px'}),
            html.H4('A última atualização feita neste website foi em abril de 2024, tendo-se previsto a emissão de dióxido de carbono de março de 2024, dado que esta informação ainda não foi revelada.', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'width': '80%', 'margin': '0 auto', 'font-family':'Arial'})
        ])
    ], style={'width': '90%', 'margin': '0 5%', 'font-family': 'Arial'}),
    
#-------------------------------------   
    
#CRIAR MENU PARA SELECIONAR O PERÍODO E ILHA A VER
    html.H3('Dados Passados', style={'color':'#069EE1', 'text-align':'center', 'margin-top': '80px', 'font-family':'Arial'}),  
    html.Div(style={'height':'20px'}),
    html.H4('Selecione a ilha que pretende visualizar e a forma como deseja comparar os dados passados (de forma mensal ou anual).', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'width': '80%', 'margin': '0 auto', 'font-family':'Arial'}),
    html.Div(style={'height':'20px'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='tempo',
                options=[
                        {'label': 'Dados Passados: 2019', 'value': '2019'},
                        {'label': 'Dados Passados: 2020', 'value': '2020'},
                        {'label': 'Dados Passados: 2021', 'value': '2021'},
                        {'label': 'Dados Passados: 2022', 'value': '2022'},
                        {'label': 'Dados Passados: 2023', 'value': '2023'},
                        {'label': 'Dados Passados: 2024', 'value': '2024'},
                        {'label': 'Dados Passados: Janeiro', 'value': 'janeiro'},
                        {'label': 'Dados Passados: Fevereiro', 'value': 'fevereiro'},
                        {'label': 'Dados Passados: Março', 'value': 'marco'},
                        {'label': 'Dados Passados: Abril', 'value': 'abril'},
                        {'label': 'Dados Passados: Maio', 'value': 'maio'},
                        {'label': 'Dados Passados: Junho', 'value': 'junho'},
                        {'label': 'Dados Passados: Julho', 'value': 'julho'},
                        {'label': 'Dados Passados: Agosto', 'value': 'agosto'},
                        {'label': 'Dados Passados: Setembro', 'value': 'setembro'},
                        {'label': 'Dados Passados: Outubro', 'value': 'outubro'},
                        {'label': 'Dados Passados: Novembro', 'value': 'novembro'},
                        {'label': 'Dados Passados: Dezembro', 'value': 'dezembro'}
                        ],
                value='2019'
            ),
        ], style = {'vertical-align':'top', 'display': 'inline-block', 'text-align':'center', 'width': '45%', 'margin-top': '10px', 'margin': '0 auto', 'font-family':'Arial'}),   
        html.Div([
            dcc.Dropdown(
                id='ilha',
                options=[
                        {'label': 'Santa Maria', 'value': 'santa_maria'},
                        {'label': 'São Miguel', 'value': 'sao_miguel'},
                        {'label': 'Terceira', 'value': 'terceira'},
                        {'label': 'Graciosa', 'value': 'graciosa'},
                        {'label': 'São Jorge', 'value': 'sao_jorge'},
                        {'label': 'Pico', 'value': 'pico'},
                        {'label': 'Faial', 'value': 'faial'},
                        {'label': 'Flores', 'value': 'flores'},
                        {'label': 'Corvo', 'value': 'corvo'}                
                        ],
                value='santa_maria'
            ),
        ], style = {'vertical-align':'top', 'display': 'inline-block', 'text-align':'center', 'width': '45%', 'margin-top': '10px', 'margin': '0 auto', 'font-family':'Arial'})
    ], style = {'vertical-align':'top', 'text-align':'center', 'margin': '0 auto'}),
    html.Div(style={'height':'20px'}),
    dcc.Tabs([
        dcc.Tab(label='Produção de Eletricidade', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            dcc.Graph(id='passado_producao', style={'maxWidth': '80%', 'margin': '0 auto'})
        ]),
        dcc.Tab(label='Emissão de Dióxido de Carbono', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            dcc.Graph(id='passado_emissao', style={'maxWidth': '80%', 'margin': '0 auto'})
        ])
    ], style={'width': '90%', 'margin': '0 5%', 'font-family': 'Arial'}),
    
#-------------------------------------   
    
#CRIAR MAPA DOS AÇORES
    html.H3('Dados Previstos', style={'color':'#069EE1', 'text-align':'center', 'margin-top': '80px', 'font-family':'Arial'}),  
    html.Div(style={'height':'20px'}),
    html.H4('Os dados previstos, relativos a março de 2024, foram obtidos através de machine learning, usando como treino e teste os dados apresentados anteriormente. Foram testados, para cada ilha e cada fonte de eletricidade, três modelos: Autoregressivo, Floresta Aleatória e Perceptron de Multicamadas, tendo-se sempre selecionado o que apresentou erros menores.', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'width': '80%', 'margin': '0 auto', 'font-family':'Arial'}),
    html.Div(style={'height':'20px'}),
    html.Div([
        dcc.Graph(
            id='map',
            figure=fig,
            style={'text-align':'center', 'width': '80%', 'margin': '0 auto'}
        )
    ]),
    html.Div(style={'height':'20px'}),
    dcc.Tabs([
        dcc.Tab(label='Produção de Eletricidade', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            dcc.Graph(
                id='previsto_producao', 
                figure=fig1,
                style={'maxWidth': '80%', 'margin': '0 auto'})
        ]),
        dcc.Tab(label='Emissão de Dióxido de Carbono', style={'color':'black', 'text-align':'center', 'margin-top': '10px', 'font-family':'Arial'}, children=[
            dcc.Graph(
                id='previsto_emissao', 
                figure=fig2,
                style={'maxWidth': '80%', 'margin': '0 auto'})
        ])
    ], style={'width': '90%', 'margin': '0 5%', 'font-family': 'Arial'})
])

#-------------------------------------   

#DEFINIR GRÁFICOS DOS DADOS PASSADOS RELATIVOS À PRODUÇÃO

cores = ['#069EE1', '#FF8C00', '#FFD700', '#4682B4', '#F4A460', '#FFFACD', '#E0FFFF']

@app.callback(
    Output('passado_producao', 'figure'),
    [Input('tempo', 'value'),
     Input('ilha', 'value')]
)

def atualizar_passado(tempo, ilha):
    if ilha == 'santa_maria':
        passado_dados = santa_maria_total #selecionar dados da ilha correspondente
        colunas = santa_maria_total.columns[4:7] #selecionar apenas as colunas relativas à produção de eletricidade
    elif ilha == 'sao_miguel':
        passado_dados = sao_miguel_total
        colunas = sao_miguel_total.columns[4:11]
    elif ilha == 'terceira':
        passado_dados = terceira_total
        colunas = terceira_total.columns[4:11]
    elif ilha == 'graciosa':
        passado_dados = graciosa_total
        colunas = graciosa_total.columns[4:7]
    elif ilha == 'sao_jorge':
        passado_dados = sao_jorge_total
        colunas = sao_jorge_total.columns[4:7]
    elif ilha == 'pico':
        passado_dados = pico_total
        colunas = pico_total.columns[4:8]
    elif ilha == 'faial':
        passado_dados = faial_total
        colunas = faial_total.columns[4:9]
    elif ilha == 'flores':
        passado_dados = flores_total
        colunas = flores_total.columns[4:8]
    elif ilha == 'corvo':
        passado_dados = corvo_total
        colunas = corvo_total.columns[4:6]
    if tempo == '2019':
        passado_dados = passado_dados[passado_dados['Ano'] == 2019] #selecionar apenas o período que se pretende
        nome = 'Mês' #selecionar a coluna que será o eixo dos x
    elif tempo == '2020':
        passado_dados = passado_dados[passado_dados['Ano'] == 2020]
        nome = 'Mês'
    elif tempo == '2021':
        passado_dados = passado_dados[passado_dados['Ano'] == 2021]
        nome = 'Mês'
    elif tempo == '2022':
        passado_dados = passado_dados[passado_dados['Ano'] == 2022]
        nome = 'Mês'
    elif tempo == '2023':
        passado_dados = passado_dados[passado_dados['Ano'] == 2023]
        nome = 'Mês'
    elif tempo == '2024':
        passado_dados = passado_dados[passado_dados['Ano'] == 2024]
        nome = 'Mês'
    elif tempo == 'janeiro':
        passado_dados = passado_dados[passado_dados['Mês'] == 1]
        nome = 'Ano'
    elif tempo == 'fevereiro':
        passado_dados = passado_dados[passado_dados['Mês'] == 2]
        nome = 'Ano'
    elif tempo == 'marco':
        passado_dados = passado_dados[passado_dados['Mês'] == 3]
        nome = 'Ano'
    elif tempo == 'abril':
        passado_dados = passado_dados[passado_dados['Mês'] == 4]
        nome = 'Ano'
    elif tempo == 'maio':
        passado_dados = passado_dados[passado_dados['Mês'] == 5]
        nome = 'Ano'
    elif tempo == 'junho':
        passado_dados = passado_dados[passado_dados['Mês'] == 6]
        nome = 'Ano'
    elif tempo == 'julho':
        passado_dados = passado_dados[passado_dados['Mês'] == 7]
        nome = 'Ano'
    elif tempo == 'agosto':
        passado_dados = passado_dados[passado_dados['Mês'] == 8]
        nome = 'Ano'
    elif tempo == 'setembro':
        passado_dados = passado_dados[passado_dados['Mês'] == 9]
        nome = 'Ano'
    elif tempo == 'outubro':
        passado_dados = passado_dados[passado_dados['Mês'] == 10]
        nome = 'Ano'
    elif tempo == 'novembro':
        passado_dados = passado_dados[passado_dados['Mês'] == 11]
        nome = 'Ano'
    elif tempo == 'dezembro':
        passado_dados = passado_dados[passado_dados['Mês'] == 12]
        nome = 'Ano'
    barras = []
    for i, coluna in enumerate(colunas):
        barra = go.Bar(x=passado_dados[nome], y=passado_dados[coluna], name=coluna, marker=dict(color=cores[i])) #ir adicionando cada coluna
        barras.append(barra)
    layout = go.Layout(
        xaxis=dict(title=nome.capitalize()),
        yaxis=dict(title='Produção de Eletricidade (kW)'),
        barmode='stack', 
        font=dict(family="Arial", color='black')
    )
    figura = go.Figure(data=barras, layout=layout)
    return figura
    
#-------------------------------------

#DEFINIR GRÁFICOS DOS DADOS PASSADOS RELATIVOS À EMISSÃO

cores = ['#069EE1', '#FF8C00', '#FFD700', '#4682B4', '#F4A460', '#FFFACD', '#E0FFFF']

@app.callback(
    Output('passado_emissao', 'figure'),
    [Input('tempo', 'value'),
     Input('ilha', 'value')]
)

def atualizar_passado(tempo, ilha):
    if ilha == 'santa_maria':
        passado_dados = santa_maria_total #selecionar dados da ilha correspondente
        colunas = santa_maria_total.columns[7:8] #selecionar apenas as colunas relativas à produção de eletricidade
    elif ilha == 'sao_miguel':
        passado_dados = sao_miguel_total
        colunas = sao_miguel_total.columns[11:14]
    elif ilha == 'terceira':
        passado_dados = terceira_total
        colunas = terceira_total.columns[11:15]
    elif ilha == 'graciosa':
        passado_dados = graciosa_total
        colunas = graciosa_total.columns[7:8]
    elif ilha == 'sao_jorge':
        passado_dados = sao_jorge_total
        colunas = sao_jorge_total.columns[7:8]
    elif ilha == 'pico':
        passado_dados = pico_total
        colunas = pico_total.columns[8:10]
    elif ilha == 'faial':
        passado_dados = faial_total
        colunas = faial_total.columns[9:11]
    elif ilha == 'flores':
        passado_dados = flores_total
        colunas = flores_total.columns[8:9]
    elif ilha == 'corvo':
        passado_dados = corvo_total
        colunas = corvo_total.columns[6:7]
    if tempo == '2019':
        passado_dados = passado_dados[passado_dados['Ano'] == 2019] #selecionar apenas o período que se pretende
        nome = 'Mês' #selecionar a coluna que será o eixo dos x
    elif tempo == '2020':
        passado_dados = passado_dados[passado_dados['Ano'] == 2020]
        nome = 'Mês'
    elif tempo == '2021':
        passado_dados = passado_dados[passado_dados['Ano'] == 2021]
        nome = 'Mês'
    elif tempo == '2022':
        passado_dados = passado_dados[passado_dados['Ano'] == 2022]
        nome = 'Mês'
    elif tempo == '2023':
        passado_dados = passado_dados[passado_dados['Ano'] == 2023]
        nome = 'Mês'
    elif tempo == '2024':
        passado_dados = passado_dados[passado_dados['Ano'] == 2024]
        nome = 'Mês'
    elif tempo == 'janeiro':
        passado_dados = passado_dados[passado_dados['Mês'] == 1]
        nome = 'Ano'
    elif tempo == 'fevereiro':
        passado_dados = passado_dados[passado_dados['Mês'] == 2]
        nome = 'Ano'
    elif tempo == 'marco':
        passado_dados = passado_dados[passado_dados['Mês'] == 3]
        nome = 'Ano'
    elif tempo == 'abril':
        passado_dados = passado_dados[passado_dados['Mês'] == 4]
        nome = 'Ano'
    elif tempo == 'maio':
        passado_dados = passado_dados[passado_dados['Mês'] == 5]
        nome = 'Ano'
    elif tempo == 'junho':
        passado_dados = passado_dados[passado_dados['Mês'] == 6]
        nome = 'Ano'
    elif tempo == 'julho':
        passado_dados = passado_dados[passado_dados['Mês'] == 7]
        nome = 'Ano'
    elif tempo == 'agosto':
        passado_dados = passado_dados[passado_dados['Mês'] == 8]
        nome = 'Ano'
    elif tempo == 'setembro':
        passado_dados = passado_dados[passado_dados['Mês'] == 9]
        nome = 'Ano'
    elif tempo == 'outubro':
        passado_dados = passado_dados[passado_dados['Mês'] == 10]
        nome = 'Ano'
    elif tempo == 'novembro':
        passado_dados = passado_dados[passado_dados['Mês'] == 11]
        nome = 'Ano'
    elif tempo == 'dezembro':
        passado_dados = passado_dados[passado_dados['Mês'] == 12]
        nome = 'Ano'
    barras = []
    for i, coluna in enumerate(colunas):
        barra = go.Bar(x=passado_dados[nome], y=passado_dados[coluna], name=coluna, marker=dict(color=cores[i]), showlegend=True) #ir adicionando cada coluna
        barras.append(barra)
    layout = go.Layout(
        xaxis=dict(title=nome.capitalize()),
        yaxis=dict(title='Emissão de Co<sub>2</sub> (g)'),
        barmode='stack', 
        font=dict(family="Arial", color='black')
    )
    figura = go.Figure(data=barras, layout=layout)
    return figura
    
#-------------------------------------

#CORRER O DASHBOARD
if __name__ == '__main__':
    app.run_server(debug=False)