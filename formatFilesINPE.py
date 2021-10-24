#!/bin/python2.7

import csv
from fire import *
from inmet import *
import os
import copy
from datetime import datetime

directory_inmet = "Data/Climate-INPE/2020"

#global fires
fires = []

one_city_inmet_list = []

def open_and_save_inmet_file(file_inmet, city):
    file = open(file_inmet)

    type(file)

    csv_reader = csv.reader(file, delimiter=";")

    rows = []
    for row in csv_reader:
        if not is_inmet_csv_header(row[0]):
            save_inmet_in_one_city_inmet_list(row, city)

    file.close()

def save_inmet_in_one_city_inmet_list(row, city):
    day = row[0]
    hour = format_hour(row[1])
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
            # print(fire.city)
            file_inmet = os.path.join(directory_inmet, filename)
            if os.path.isfile(file_inmet):
                city_inmet = fire.city
                open_and_save_inmet_file(file_inmet, city_inmet)
                return True
    return False

def assign_inmet_to(fire):
    for inmet_entry in one_city_inmet_list:
        if (inmet_entry.day == fire.day) and (inmet_entry.hour == fire.hour):
            fire.inmet = copy.deepcopy(inmet_entry)
    
    del one_city_inmet_list [:]

def save_fire_in_fires_list(row):
    list_day_hour = row[0].split(" ")
    day = list_day_hour[0]
    hour = format_hour(list_day_hour[1])
    state = row[3].upper()
    city = row[4].upper()
    bioma = row[5].upper()
    days_without_rain = row[6]
    precipitation = row[7]
    fire_risk = row[8]
    latitude = row[9]
    longitude = row[10]
    frp = row[11]
    fire = Fire(day, hour, city, bioma, days_without_rain, precipitation, fire_risk, latitude, longitude, frp, None)
    fires.append(fire)

def format_hour(hour):
    return hour[0] + hour[1] + "00" 

def calculate_miss():
    cities = {}
    for filename in os.listdir(directory_inmet):
        try:
            filename_list = filename.split("_")
            file_city = filename_list[4]
            cities[file_city] = 0
        except Exception as exc:
            print(exc)

    total = len(fires)
    found = 0
    miss = 0
    missing_cities = {}
    for fire in fires:
        if fire.city in cities:
            cities[fire.city] += 1
            found += 1
        else:
            miss += 1
            missing_cities[fire.city] = missing_cities.get(fire.city, 0) + 1
            
        if (found + miss) % 100 == 0:
            print('{} - {}/{}'.format(datetime.now(), found+miss, total))
    print('{} - {}/{}'.format(datetime.now(), found+miss, total))
    print('{} - End: Fire Records -  Total: {}, Founded: {} / misses: {}'.format(datetime.now(), total, found, miss))
    print('{} - Number of Cities {}'.format(datetime.now(), len(cities)))
    print('{} - Cities Missing {}'.format(datetime.now(), len(missing_cities)))    

if "__main__":
    open_file_fires()
    #print(fires[0].city)
    found = 0
    miss = 0
    cities_missing = {}
    total = len(fires)
    print('{} - Starting'.format(datetime.now()))
    calculate_miss()

    """
    print(fires[0].__str__())
    for fire in fires:
        if save_inmet_file_related_to(fire):
            assign_inmet_to(fire)
            found += 1
            # break
        else:
            miss += 1
            if fire.city not in cities_missing:
                cities_missing[fire.city] = ''
        # print('.', end=' ')
        if (found + miss) % 100 == 0:
            print('{} - {}/{}'.format(datetime.now(), found+miss, total))
    """
    print(cities_missing)
    print("{}/{} - from total of {}".format(found, miss, total))