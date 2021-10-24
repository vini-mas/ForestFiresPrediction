import csv
from fire import *
import os

directory_inmet = "Data/Climate-INPE/2020"

#global fires
fires = []

def open_file_inmet():
    file = open("Data/Climate-INPE/2020/INMET_CO_DF_A042_BRAZLANDIA_01-01-2020_A_31-12-2020.CSV")

    type(file)

    csv_reader = csv.reader(file)

    header = []
    for header in csv_reader:
        header = next(csv_reader)
        print(header)


    rows = []
    for row in csv_reader:
        rows.append(row)
    print(rows[0])

    file.close()


def is_fire_csv_header(name):
    return name == "datahora"


def open_file_fires():
    file = open("Data/FiresOutbreaks-INPE/Focos_2020-01-01_2020-12-31.csv")

    type(file)

    csv_reader = csv.reader(file)

    rows = []
    for row in csv_reader:
        rows.append(row)
        if not is_fire_csv_header(row[0]): 
            save_fire_in_fires_list(row)
        

    print(rows[0])
    print(rows[1])

    file.close()


#filename --> INMET_S_RS_A810_SANTA ROSA_01-01-2020_A_31-12-2020.CSV
#filename_list --> ['INMET', 'S', 'RS', 'A810', 'SANTA ROSA', '01-01-2020', 'A', '31-12-2020.CSV']
#file_city --> SANTA ROSA
def assign_inmet_to_fire():
    for filename in os.listdir(directory_inmet):
        try:
            filename_list = filename.split("_")
            file_city = filename_list[4]
            print(file_city)
        except:
            pass

def save_fire_in_fires_list(row):
    list_day_hour = row[0].split(" ")
    day = list_day_hour[0]
    hour = list_day_hour[1]
    city = row[4]
    fire = Fire(day, hour, city, None)
    fires.append(fire)

if "__main__":
    open_file_fires()
    print(fires[0].city)
    assign_inmet_to_fire()