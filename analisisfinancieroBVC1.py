#Programa para hacer analisis de mercados financieros con la libreria yfinance

#Se debe instalar los siguientes paquetes:
#pip install yfinance pandas matplotlib numpy

import yfinance as yf
import pandas as pd
import numpy as np

#Intentamos crear un objeto Ticker para la Bolsa de Valores de Caracas
ticker_bvc = yf.Ticker("BVCC.CR")

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
    