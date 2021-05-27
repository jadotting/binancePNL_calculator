import csv
import pandas as pd

from datetime import datetime

crypto_profit = "Export Order History.xlsx"

list_of_buy_or_sell = []

list_of_price = []

list_of_status = []

header_row = []

def remove_duplicates(x): 
  return list(dict.fromkeys(x))

def for_csv_file(file):
    pnl = 0
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=
                                ',')
        line_count = 0
        column_where_type_is = -1
        column_where_price_is = -1
        column_where_status_is = -1
        counter = -1
        for row in csv_reader:
            #header line
            if line_count == 0:
                header_row=row
                for i in row:
                    counter = counter + 1
                    if (i.replace(" ", "").lower() == 'type'):
                        column_where_type_is = counter
                    if (i.replace(" ", "").lower() == 'total'):
                        column_where_price_is = counter
                    if (i.replace(" ", "").lower() == 'status'):
                        column_where_status_is = counter
                    if (column_where_type_is != -1 and column_where_price_is != -1 and column_where_status_is != -1):
                      break;
                line_count = line_count + 1
            #values line
            else:
                list_of_buy_or_sell.append(row[column_where_type_is])
                list_of_price.append(row[column_where_price_is])
                list_of_status.append(row[column_where_status_is])
    #calculate p&l         
    for column_number, oneValue in enumerate(list_of_buy_or_sell):
        buy_or_sell = oneValue
        trade_status = list_of_status[column_number]
        if buy_or_sell.replace(" ", "").lower() == 'buy':
          if trade_status.replace(" ", "").lower() == 'filled':
            pnl -= float(list_of_price[column_number])
        if buy_or_sell.replace(" ", "").lower() == 'sell':
          if trade_status.replace(" ", "").lower() == 'filled':
            pnl += float(list_of_price[column_number])
    return pnl
            
def for_xlsx_file(filename):
    header_row = []
    row = []
    rows = []
    data = pd.read_excel(filename)
    filename_split = filename.split('.')
    filename_csv = filename_split[0] + '.csv'
    data.to_csv(filename_csv, index = None, header=True)
    return filename_csv
  
#main
if 'xlsx' or 'xls' in cryto_profit:
      filename_csv = for_xlsx_file(crypto_profit)
      pnl = for_csv_file(filename_csv)
      print(pnl)
else:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log_string = "[" + dt_string +"] " + "PLEASE MAKE SURE FILE EXTENSIONS ARE XLSX \n"
    log_file = open("log.txt","a")
    log_file.write(log_string)    

