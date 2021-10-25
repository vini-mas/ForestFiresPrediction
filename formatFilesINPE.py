#!/bin/python2.7

import csv
from fire import *
from inmet import *
import os
import copy
from datetime import datetime

# DEBUG
PRINT_HEADER=False

FORCE_LIMIT = False

LIMIT = None
LIMIT_INMET = None

if FORCE_LIMIT:
    LIMIT = 5000
    LIMIT_INMET = 20

# CONSTANTS
directory_inmet = "Data/Climate-INPE/2020"

OUTPUT_CSV = 'Data/proccessed.csv'

#global fires
fires = []

one_city_inmet_list = []

cities_inmet = {}

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
    inmet = Inmet.init(row, city)
    one_city_inmet_list.append(inmet)

def is_inmet_csv_header(name):
    return name in ["REGIAO:", "UF:", "ESTACAO:", "CODIGO (WMO):", "LATITUDE:", "LONGITUDE:", "ALTITUDE:", "DATA DE FUNDACAO:", "Data"]

def is_fire_csv_header(name):
    return name == "datahora"


def read_file_fires():
    file = open("Data/FiresOutbreaks-INPE/Focos_2020-01-01_2020-12-31.csv")

    type(file)

    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not is_fire_csv_header(row[0]): 
            save_fire_in_fires_list(row)

    file.close()


def read_inmet_files():
    for file_index, filename in enumerate(os.listdir(directory_inmet)):
        try:
            filename_list = filename.split("_")
            city = filename_list[4]

            file_path = os.path.join(directory_inmet, filename)
            if os.path.isfile(file_path):
                print('Reading: {}'.format(city))
                with open(file_path) as file:
                    csv_reader = csv.reader(file, delimiter=";")
                    lista = list(csv_reader)

                    # removing headers and column name from csv       
                    for index, value in enumerate(lista):
                        if 'Data' in value:
                            break
                    
                    if PRINT_HEADER:
                        for i, value in enumerate(lista[index]):
                            print('{} - {}'.format(i, value))
                    
                    lista = lista[index+1:]
                    
                    cities_inmet[city] = map(lambda x: Inmet.init(x, city), lista)
        except:
            pass

        if LIMIT_INMET and file_index > LIMIT_INMET:
            print("BREAK")
            break


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
    for inmet_entry in cities_inmet.get(fire.city):
        if (inmet_entry.day == fire.day) and (inmet_entry.hour == fire.hour) and '' not in inmet_entry.to_csv():
            fire.inmet = copy.deepcopy(inmet_entry)

def save_fire_in_fires_list(row):
    fire = Fire.init(row)
    fires.append(fire)

def format_hour(hour):
    return hour[0] + hour[1] + "00" 


def statistics():
    print('{} - Calculating from FIRE'.format(datetime.now()))
    hits = 0
    valid = None
    for index, fire in enumerate(fires):
        if fire.inmet:
            hits += 1
            valid = index
    
    print('hits: {}/{} total'.format(hits, len(fires)))


def calculate_miss():
    total = len(fires)
    found = 0
    miss = 0

    missing_cities = {}
    cities = {}

    for fire in fires:
        if fire.city in cities_inmet:
            cities[fire.city] = cities.get(fire.city, 0) + 1
            found += 1
        else:
            miss += 1
            missing_cities[fire.city] = missing_cities.get(fire.city, 0) + 1

    print('{} - Fire Records\n\tTotal: {}, \n\tFounded: {} / misses: {}'.format(datetime.now(), total, found, miss))
    print('{} - Number of Cities hited {} vs cities at INMET: {}'.format(datetime.now(), len(cities), len(cities_inmet)))
    print('{} - Cities Missing {}'.format(datetime.now(), len(missing_cities)))    


def main():
    print('{} - Reading fires files'.format(datetime.now()))
    read_file_fires()

    print('{} - Reading inmet files'.format(datetime.now()))
    read_inmet_files()

    print('{} - Assigning inmet to FIRES'.format(datetime.now()))
    total = len(fires)

    for index, fire in enumerate(fires):
        if fire.city in cities_inmet:
            assign_inmet_to(fire)

        if LIMIT and index > LIMIT:
            print('ABORT')
            break

        if index % 100 == 0:
            percentage = float(index)/float(total)
            print('{:.1f}% - {}/{}'.format(percentage*100, index, total))

    fires_hitted = list(filter(lambda x: x.inmet, fires))
    header = fires_hitted[0].to_csv_header() + fires_hitted[0].inmet.to_csv_header()

    body = []
    for fire in fires_hitted:
        b = fire.to_csv() + fire.inmet.to_csv()
        body.append(b)
    

    with open(OUTPUT_CSV, 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(body)

    print('{} - Calculating misses'.format(datetime.now()))
    calculate_miss()

    statistics()

    # print(json.dumps(body, indent=True))

if "__main__":
    main()