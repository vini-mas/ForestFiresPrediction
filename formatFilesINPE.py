import csv
from fire import *
from inmet import *
import os

directory_inmet = "Data/Climate-INPE/2020"

#global fires
fires = []

one_city_inmet_list = []

city_inmet = ""

def open_and_save_inmet_file(file_inmet):
    file = open(file_inmet)

    type(file)

    csv_reader = csv.reader(file, delimiter=";")

    rows = []
    for row in csv_reader:
        if not is_inmet_csv_header(row[0]):
            save_inmet_in_one_city_inmet_list(row)

    file.close()

def save_inmet_in_one_city_inmet_list(row):
    day = row[0]
    hour = format_hour(row[1])
    city = city_inmet
    inmet = Inmet(day, hour, city)
    one_city_inmet_list.append(inmet)

def is_inmet_csv_header(name):
    return name in ["REGIAO:", "UF:", "ESTACAO:", "CODIGO (WMO):", "LATITUDE:", "LONGITUDE:", "ALTITUDE:", "DATA DE FUNDACAO:", "Data"]

def is_fire_csv_header(name):
    return name == "datahora"


def open_file_fires():
    file = open("Data/FiresOutbreaks-INPE/Focos_2020-01-01_2020-12-31.csv")

    type(file)

    csv_reader = csv.reader(file)

    rows = []
    for row in csv_reader:
        if not is_fire_csv_header(row[0]): 
            save_fire_in_fires_list(row)

    file.close()


#filename --> INMET_S_RS_A810_SANTA ROSA_01-01-2020_A_31-12-2020.CSV
#filename_list --> ['INMET', 'S', 'RS', 'A810', 'SANTA ROSA', '01-01-2020', 'A', '31-12-2020.CSV']
#file_city --> SANTA ROSA
#file_inmet --> Data/Climate-INPE/2020/INMET_S_RS_A810_SANTA ROSA_01-01-2020_A_31-12-2020.CSV
def save_inmet_file_related_to(fire):
    for filename in os.listdir(directory_inmet):
        try:
            filename_list = filename.split("_")
            file_city = filename_list[4]
        except:
            pass

        if(fire.city == file_city):
            print(fire.city)
            file_inmet = os.path.join(directory_inmet, filename)
            if os.path.isfile(file_inmet):
                open_and_save_inmet_file(file_inmet)
                return True
    return False

def assign_inmet_to(fire):
    for inmet_entry in one_city_inmet_list:
        print(inmet_entry.hour, fire.hour)
        if (inmet_entry.day == fire.day) and (inmet_entry.hour == fire.hour):
            print("found")
            #fire.inmet = copy.deepcopy(inmet_entry)
    
    del one_city_inmet_list [:]
    city_inmet = ""

def save_fire_in_fires_list(row):
    list_day_hour = row[0].split(" ")
    day = list_day_hour[0]
    hour = format_hour(list_day_hour[1])
    city = row[4].upper()
    fire = Fire(day, hour, city, None)
    fires.append(fire)

def format_hour(hour):
    return hour[0] + hour[1] + "00" 

if "__main__":
    open_file_fires()
    #print(fires[0].city)
    for fire in fires:
        if save_inmet_file_related_to(fire):
            assign_inmet_to(fire)
            break