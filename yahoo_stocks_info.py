'''
Created on Jan 10, 2021

@author: Linda Fan
'''
#imports
import requests
import time
import json


file = open("secret.txt","r+")
SECRET = file.readline()
file.close()

def get_data(symbol: str):
    ''' Takes the symbol of the stock to request the most recent stock data for the given symbol from the RapidAPI Yahoo-Finance API'''
    #Save the given symbol under sym
    sym = symbol
    #Constant required parameters
    base_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"
    required = {    'x-rapidapi-key': "SECRET",
                    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"}
    while True:
        try:
            #From the given parameter, create the query parameters, 
            # send a request to the API with all of the call's necessary parameters, 
            #and return the most recent's day's stock data for the symbol along with the symbol of the stock
            
            search_parameters = [('symbol', sym)]
            feedback = requests.request("GET", base_url, headers=required, params=search_parameters)
            return [feedback.json()["prices"][0], sym]
            
        #If we recieve a JSONDecodeError, our user must have inputed the wrong stock symbol
        except json.decoder.JSONDecodeError:
            #Inform the User that we cannot find stock data for their given symbol
            print(f'Cannot find stocks for {sym}.')
            #Ask the user to input a new symbol for the API to fetch requests for and save it under sym
            sym = get_symbol()
        
def get_symbol():
    '''Asks the user to input their stock symbol and return the user's input'''
    symbol = input("Enter your stock symbol: ")
    return symbol;  

def get_today_stocks(info: [dict]):
    '''From the given data and symbol, creates a dictionary of the relevant information from today's stock 
        and returns that dictionary with the given symbol'''
    #Create parameter data which will represent the most recent stock data
    data = info[0]
    #Find the respective times from the day the data came from and today in terms of local time
    data_time = time.localtime(data['date'])
    today_time = time.localtime()
    #Create an empty dictionary that will represent today's stock data
    results = dict()
    #If today's date and the stock's date match, store a dictionary of today's high, low, open, and close in results
    if(today_time.tm_mon == data_time.tm_mon and today_time.tm_mday == data_time.tm_mday and today_time.tm_year == data_time.tm_year):
        results = {'high': data['high'], 'low' : data['low'], 'open': data['open'] , 'close': data['close']}
    #Return the results along with its corresponding symbol
    return [results, info[1]]
    

if __name__ == '__main__':
    #Ask the user to input their given stock symbol and find today's stock information based on the symbol
    sym = get_symbol()
    dta = get_data(sym)
    results = get_today_stocks(dta)
    today_stk = results[0]
    sym = results[1]
    #If the today_stk is an empty dictionary, this indicate that stock trading did not happen today. Inform the user.
    if today_stk == dict():
        print(f"No {sym.upper()} stocks were traded today.")
    #Otherwise, inform the user of their symbol's respective stock information regarding today's open, high, low, and close
    else:
        print(f"Today's Stock Values for {sym.upper()}: Open: {today_stk['open']}, High: {today_stk['high']}, Low: {today_stk['low']}, Close: {today_stk['close']}")
    
    
    
