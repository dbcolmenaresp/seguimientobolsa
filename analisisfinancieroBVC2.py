#Programa para hacer analisis de mercados financieros con la libreria yfinance
#Se importan las librerias basicas
#Se importa la libreria yfinance
#Se crea un ticker para hacer el seguimiento de una acción (BVCC)
#Se consulta el historico de precios del ticker indicado
#Se analizan algunos datos para el analisis fundamental (estado de resultados, balance general, flujo de efectivo)

#Se debe instalar los siguientes paquetes:
#pip install yfinance pandas matplotlib numpy

import yfinance as yf
import pandas as pd
import numpy as np

# Leer el Ticker desde el teclado

try:
    # Solicitar el Ticker al usuario
    nombre = input("Ingrese el Ticker a consultar: ")

    # Mostrar el dato ingresado
    print(f"Ticker analizado: {nombre}")


    #Intentamos crear un objeto Ticker para la Bolsa de Valores de Caracas
    ticker_bvc = yf.Ticker(nombre)

    #El directorio .info contiene metadatos, pero para la BVC puede estar muy vacio
    info = ticker_bvc.info
    print(f"Nombre: {info.get('longName', 'No disponible')}")
    print(f"Sector: {info.get('sector', 'No disponible')}")

    #Descargar el ultimo año de datos historicos
    hist = ticker_bvc.history(period="1y")
    if not hist.empty:
        print(hist.tail()) #Muestra los ultimos 5 dias de cotizacion
    else:
        print("No se encontraron datos historicos para este tickeren Yahoo Finance.")
    
    #Analisis fundamental
    try:
        #Estado de resultados (Income Statement)
        income_stmt = ticker_bvc.income_stmt
        if not income_stmt.empty:
            print("---Estado de Resultados (Anual) ---")
            print("income_stmt.loc[['Total Revenue', 'Net Income']]")
        #Balance general (Balance sheet)
        balance_sheet = ticker_bvc.balance_sheet
        if not balance_sheet.empty:
            print("\n--- Balance General (Anual) ---")
            print(balance_sheet.loc[['Total Assets', 'Total Deb']])
        
        #Flujo de efectivo
        cashflow = ticker_bvc.cashflow
        if not cashflow.empty:
            print("\n--- Flujo de Efectivo (Anual) ---")
            print(cashflow.loc[['Operating Cash Flow', 'Capital Expenditure']])

    except Exception as e:
        print(f"Error al obtener estados financieros: {e}. La empresa puede no reportar a Yahoo Finance")
    
    #Obtener el precio actual de la accion
    
    precio_actual = hist['Close'].iloc[-1] if not hist.empty else None

    #Intentar obtener el EPS (beneficio por acción) desde el método .info
    eps = info.get('trailingEps')
    if precio_actual and eps and eps != 0:
        per = precio_actual / eps
        print(f"PER calculado: {per:.2f}")
    else:
        print("No hay suficientes datos para calcular el PER (falta EPS o precio).")
    
    #Calculo manual del ROE usando el Estado de Resultados y el Balance
    #Requiere que income_stmt y balance_sheet tengan datos
    #ROE = Net Income / Total Stockholders Equity
    
except Exception as e:
    # Captura cualquier error inesperado
    print(f"Ocurrió un error: {e}")
