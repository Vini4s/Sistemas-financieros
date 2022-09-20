#Librerias
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

#Menu de las empresas
Menu=["AAPL","AMZN","UBER","WMT","SBUX","TSLA","PANW","MRNA","MSFT","GOOG"]

#Menu para la gráfica
Menup=["AAPL\nApple","AMZN-Amazon","UBER-Uber","WMT-Walmart","SBUX-Starbucks","TSLA-Tesla",
"PANW-Palo Alto Networks","MRNA-Moderna","MSFT-Microsoft","GOOG-Google"]

#Se crea el Data Frame que recibira la información de las empresas
df=pd.DataFrame()

#Se crera una función para calcular la WMA a 28 días
#Se daran pesos lineales
def VWMA_28(V,C):
    MUL=V*C
    Pond=(MUL.rolling(window=28).sum())/(V.rolling(window=28).sum())
    return Pond

#Se crea un ciclo para calcular y gráficar la SMA, EMA y WMA de cada empresa
for empresa in Menu:
    df=yf.Ticker(empresa).history(start="2020-01-01",end="2023-01-01")
    df=df[["Close","Volume"]]
    #EMA
    df["EMA-26"]=df.iloc[:,0].ewm(span=26,adjust=False).mean()
    df["EMA-12"]=df.iloc[:,0].ewm(span=12,adjust=False).mean()

    #MACD
    df["MACD"]=df["EMA-12"]-df["EMA-26"]

    #SEÑAL-9 periodos
    df["SEÑAL"]=df.iloc[:,4].ewm(span=9,adjust=False).mean()

    #HISTOGRAMA
    df["HISTOGRAMA"]=df["MACD"]-df["SEÑAL"]

    #VWMA
    df["VWMA-28"]=VWMA_28(df["Volume"],df["Close"])

    #Primer gráfico
    Grafico=plt.figure(figsize=(10,6))
    Tabla=gridspec.GridSpec(nrows=2,ncols=1,figure=Grafico,height_ratios=[2,1])
    Graf_SUP=plt.subplot(Tabla[0,0])
    Graf_SUP.plot(df["EMA-12"],label='EMA-12',color="orange")
    Graf_SUP.plot(df["EMA-26"],label='EMA-26',color="black")
    Graf_SUP.plot(df["Close"],label='Cierre',color="yellow")
    Graf_SUP.plot(df["VWMA-28"],label='VWMA-28',color="gray")
    Graf_SUP.set_title(Menup[Menu.index(empresa)])
    Graf_SUP.grid()
    Graf_SUP.legend()

    Graf_INF=plt.subplot(Tabla[1,0])
    Graf_INF.plot(df["MACD"],label='MACD',color="blue")
    Graf_INF.plot(df["SEÑAL"],label='SEÑAL',color="green")
    Graf_INF.bar(df.index,df["HISTOGRAMA"],color="gray",label="HIST")
    Graf_INF.set_title("MACD, SEÑAL E HISTOGRAMA")
    Graf_INF.legend()

    plt.grid()
    plt.show()