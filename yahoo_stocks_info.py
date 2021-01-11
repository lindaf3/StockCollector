'''
Created on Jan 10, 2021

@author: Linda Fan
'''
#imports
import requests
import time
import json



def get_data(symbol: str):
    ''' Takes the symbol of the stock to request from Yahoo Finance a JSONFile of its historical data'''
    sym = symbol
    base_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"
    required = {    'x-rapidapi-key': "883f54a2eemshc4d6fd4695f96aap1cf784jsn76c6b3c90387",
                    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"}
    feedback = None
    while True:
        try:
            search_parameters = [('symbol', sym)]
            feedback = requests.request("GET", base_url, headers=required, params=search_parameters)
            return [feedback.json()["prices"][0], sym]
        except json.decoder.JSONDecodeError:
            print(f'Cannot find stocks for {sym}.')
            sym = get_symbol()
        
def get_symbol():
    '''Asks the user to input their stock symbol and return the uer's input'''
    symbol = input("Enter your stock symbol: ")
    return symbol;  

def get_today_stocks(info: [dict]):
    data = info[0]
    data_time = time.localtime(data['date'])
    today_time = time.localtime()
    results = dict()
    if(today_time.tm_mon == data_time.tm_mon and today_time.tm_mday == data_time.tm_mday and today_time.tm_year == data_time.tm_year):
        results = {'high': data['high'], 'low' : data['low'], 'open': data['open'] , 'close': data['close']}
    return [results, info[1]]
    

if __name__ == '__main__':
    sym = get_symbol()
    dta = get_data(sym)
    results = get_today_stocks(dta)
    today_stk = results[0]
    sym = results[1]
    if today_stk == dict():
        print(f"No {sym} stocks were traded today.")
    else:
        print(f"Today's Stock Values for {sym}: High: {today_stk['high']}, Low: {today_stk['low']}, Open: {today_stk['open']}, Close: {today_stk['close']}")
    
    
    