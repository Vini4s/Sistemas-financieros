#Librerias
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
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
def WMA_28(Pesos):
    def f(x):
        return sum(Pesos*x)/sum(Pesos)
    return f
#Se crean los pesos
periodo=28
Pesos=list(reversed([(periodo-n)*periodo for n in range(periodo)]))

#Se crea un ciclo para calcular y gráficar la SMA, EMA y WMA de cada empresa
for empresa in Menu:
    df=yf.Ticker(empresa).history(start="2020-01-01",end="2023-01-01")
    df=df[["Close"]]
    #SMA
    df["SMA-28"]=df.iloc[:,0].rolling(window=28).mean()

    #EMA
    df["EMA-28"]=df.iloc[:,0].ewm(span=28,adjust=False).mean()

    #WMA
    df["WMA-28"]=df.iloc[:,0].rolling(window=28).apply(WMA_28(Pesos), raw=True)
    
    plt.plot(df["SMA-28"],label='SMA-28 dias',color="blue")
    plt.plot(df["EMA-28"],label='EMA-28 dias',color="orange")
    plt.plot(df["WMA-28"],label='WMA-28 dias',color="green")
    plt.title(Menup[Menu.index(empresa)])
    plt.grid()
    plt.ylabel("Precio dolares")
    plt.legend()
    plt.show()
