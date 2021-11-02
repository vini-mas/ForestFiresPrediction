from enum import Enum
import os
from typing import List
import pandas as pd
from pathlib import Path
from pandas.core.frame import DataFrame

from model.inmet import Inmet
from model.yearly_inmet import YearlyInmet
from model.fire_outbreaks import FireOutbreaks
from data_manager.helper import Helper


class DataManager:
    inmet_list: List[Inmet] = []
    yearly_inmet_list: List[YearlyInmet] = []
    fire_outbreaks_list: List[FireOutbreaks]

    year_to_process: str

    fire_outbreaks_path: str
    inmet_path: str

    helper: Helper

    def __init__(self, fire_outbreaks_path: str, inmet_path: str, year_to_process: str):
        self.fire_outbreaks_path = fire_outbreaks_path
        self.inmet_path = inmet_path
        self.year_to_process = year_to_process
        self.helper = Helper()

    def get_fire_outbreaks_df(self, fire_outbreaks: FireOutbreaks):
        return pd.DataFrame(fire_outbreaks.df_list, columns=fire_outbreaks.df_columns)

    def get_inmet_df(self, inmet: Inmet):
        return pd.DataFrame(inmet.df_list, columns=inmet.df_columns)
    
    ## Create and Save a Full Centralized DataFrame merging Fire Outbreaks and closest Inmet
    # Save additional files by (State, City, Biome) in the process
    # DataFrame Columns: 
    # ['date', 'state', 'city', 'biome', 'latitude', 'longitude', 'fire_power', 'had_fire_outbreak'
    # 'precip_sum', 'temp_mean', 'temp_median', 'max_temp', 'min_temp', 'max_hum_max', 'min_hum', 
    # 'hum_mean', 'hum_median', 'wind_mean', 'wind_median', 'wind_max', 'wind_min', 'had_min_rain', 
    # 'had_strong_rain', 'days_wo_rain', 'days_wo_strong_rain', 'latitude_inmet', 'longitude_inmet']
    def process_centralized_data(self):
        
        # Progress Bar
        bar = self.helper.initialize_progress_bar(
            f'\n({self.year_to_process}) Creating {len(self.fire_outbreaks_list)} centralized dataframes...', size=len(self.fire_outbreaks_list))

        full_centralized_df: DataFrame = DataFrame()

        # Merge each FireOutbreak with closest Inmet
        for index, fire_outbreaks_v3 in enumerate(self.fire_outbreaks_list):
            bar.update(index)

            yearly_inmet_index = self.helper.get_yearly_inmet_index_by_year(self.yearly_inmet_list, fire_outbreaks_v3.year)
            
            # Prepare list of Inmet coordinates
            inmet_coords: List[tuple(float, float)] = [ ]
            indexes: List[int] = []
            for i, inmet in enumerate(self.yearly_inmet_list[yearly_inmet_index].inmet_list):
                inmet_coords.append((inmet.latitude, inmet.longitude))
                indexes.append(i)

            # Find closest Inmet coordinates
            closest_inmet_index = self.helper.find_index_from_closest_coordinate(
                (fire_outbreaks_v3.latitude, fire_outbreaks_v3.longitude), inmet_coords)

            # Merge Fire Outbreaks with closest Inmet and sort by date
            centralized_df = pd.merge(
                left=self.get_fire_outbreaks_df(fire_outbreaks_v3), 
                right=self.get_inmet_df(self.yearly_inmet_list[yearly_inmet_index].inmet_list[closest_inmet_index]), 
                how='outer', on=['date'], suffixes=('_fire', '_inmet'))
            centralized_df['date'] = pd.to_datetime(centralized_df['date'], format='%Y-%m-%d')
            centralized_df = centralized_df.sort_values(by=['date'])

            centralized_df['had_fire_outbreak'] = centralized_df['had_fire_outbreak'].fillna(False)
            
            # Remove empty on temp_mean (needed to avoid saving/using files from below)
            centralized_df = centralized_df[centralized_df['temp_mean'].notnull()]

            # Avoid saving/using files without rows from inner join of inmet and fire outbreaks data
            only_inmet_df = centralized_df[centralized_df['fire_power'].notnull()]
            if(not only_inmet_df.empty):
                # Save Centralized DataFrame
                (year, state, city, biome) = (fire_outbreaks_v3.year, fire_outbreaks_v3.state, fire_outbreaks_v3.city, fire_outbreaks_v3.biome)
                
                Path(f'centralized_data/{year}').mkdir(parents=True, exist_ok=True)
                centralized_df.to_csv(f'centralized_data/{year}/centralized_{state}-{city}-{biome}.csv', index=False)

                # Append to full centralized DataFrame
                if(not full_centralized_df.empty): 
                    full_centralized_df = full_centralized_df.append(centralized_df.copy())
                else: full_centralized_df = centralized_df.copy()
        bar.finish()
        
        if(not full_centralized_df.empty):
            print(f'Saving full centralized ({len(full_centralized_df.index)} rows)...')
            # Save full centralized DataFrame
            full_centralized_df = full_centralized_df.sort_values(by=['date'])
            Path(f'centralized_data/full').mkdir(parents=True, exist_ok=True)
            full_centralized_df.to_csv(f'centralized_data/full/centralized_{year}.csv', index=False)
            print('Done.')
        else: print('({self.year_to_process}) Processed centralized resulted in empty data')


    ## Load Fire Outbreak file
    # and Creates a List of FireOutbreaks
    def process_fire_outbreaks(self):        
        # Select file name
        file_name = next(filter(lambda x: x.split('_')[1][0:4] == self.year_to_process, os.listdir(self.fire_outbreaks_path)))

        year = file_name.split('_')[1][0:4]
        self.fire_outbreaks_list = self.load_to_df_fire_outbreaks(file_name, year)
  
    ## Get the coordinates from initial header of an Inmet csv file
    def get_coord_from_inmet_file(self, foldername: str, file_name: str):        
        # Reading Longitude Latitude Information
        header_df = pd.read_csv(f'{self.inmet_path}/{foldername}/{file_name}',
                                encoding="ISO-8859-1", skiprows=3, nrows=5, sep=';', names=['info', 'value'])
        latitude = round(
            float(header_df.at[1, 'value'].replace(',', '.')), 2)
        longitude = round(
            float(header_df.at[2, 'value'].replace(',', '.')), 2)
        
        return (latitude, longitude) #(foldername, file_name, (latitude, longitude))

    ## Load each Inmet file from selected files 
    # and save as List[YearlyInmet]
    def process_inmet(self):
        file_name_list = os.listdir(f'{self.inmet_path}/{self.year_to_process}')

        # Progress Bar
        bar = self.helper.initialize_progress_bar(
            f'\n({self.year_to_process}) Loading {len(file_name_list)} Inmet files...', size=len(file_name_list))

        inmet_df = []
        yearly_inmet_list: List[YearlyInmet] = []

        # Iterate over files
        for index, file_name in enumerate(file_name_list):
            # Concat with upcoming Inmet
            inmet_df = self.load_to_df_inmet(self.year_to_process, file_name)

            yearly_index = self.helper.get_yearly_inmet_index_by_year(yearly_inmet_list, year=self.year_to_process)
            if(yearly_index != -1):
                yearly_inmet_list[yearly_index].inmet_list.append(inmet_df)
            else:
                yearly_inmet_list.append(YearlyInmet(self.year_to_process, [inmet_df]))

            bar.update(index+1)

        bar.finish()

        # Save Inmet List
        self.yearly_inmet_list = yearly_inmet_list

    ## Load Fire Outbreaks csv file and convert to List[FireOutbreaks]
    ## Columns: date state city biome latitude longitude fire_power had_fire_outbreak
    def load_to_df_fire_outbreaks(self, file_name: str, year: str):
        column = Enum(
            'Column',
            'date satelite country state city biome days_wo_rain precip fire_risk latitude longitude fire_power')
        df = pd.read_csv(f'{self.fire_outbreaks_path}/{file_name}',
                         dtype={'datetime': 'str'}, skiprows=1, names=[e.name for e in column], na_values=-999)

        # Drop Unused Columns
        dropped_columns = [column.satelite, column.country,
                           column.days_wo_rain, column.precip, column.fire_risk]
        df = df.drop(columns=[e.name for e in dropped_columns])

        # Format Date to YYYY-MM-DD
        df[column.date.name] = df[column.date.name].str.slice(0, 10).replace('/','-')

        # Format Latitude and Longitude
        for col in [column.latitude, column.longitude]:
            # Round 00.00 having error rate of max ~1km
            df[col.name] = pd.to_numeric(
                df[col.name], errors='coerce').map(lambda x: round(x, 2))

        # Merge duplicated dates
        df = df.groupby(['date', 'state', 'city', 'biome'], as_index=True).agg({
            column.latitude.name: 'mean',
            column.longitude.name: 'mean',
            column.fire_power.name: 'mean'}).reset_index()
        
        # Add Column had_fire_outbreak        
        df['had_fire_outbreak'] = True

        mean_coord_df = df[['state', 'city', 'biome', 'latitude', 'longitude']].groupby(['state', 'city', 'biome']).agg({
            column.latitude.name: 'mean',
            column.longitude.name: 'mean'}
            )
        
        mean_coord_df = mean_coord_df.reset_index()

        grouped = df.groupby(['state', 'city', 'biome'])        

        # Progress Bar
        bar = self.helper.initialize_progress_bar(
            f'\n({self.year_to_process}) Processing {len(grouped)} Fire Outbreaks grouped by (state, city, biome)...', size=len(grouped))
        countBar = 0

        #Create FireOutbreaks by grouped dataframe by ['state', 'city', 'biome']
        fire_outbreaks_list: List[FireOutbreaks] = []        
        for group_name, df_group in grouped:
            mean_coord = mean_coord_df[(mean_coord_df['state'] == group_name[0]) & (mean_coord_df['city'] == group_name[1]) & (mean_coord_df['biome'] == group_name[2])].iloc[0]
            new_fire_outbreak = FireOutbreaks(
                    year,
                    state=group_name[0], 
                    city=group_name[1], 
                    biome=group_name[2],
                    latitude=mean_coord['latitude'],
                    longitude=mean_coord['longitude'],
                    df_list=df_group.values.tolist(),
                    df_columns=df_group.columns)
            fire_outbreaks_list.append(new_fire_outbreak)
            countBar += 1
            bar.update(countBar)
        bar.finish()

        return fire_outbreaks_list    

    ## Load Inmet csv file and convert to Inmet
    ## Dataframe Columns: date precip_sum temp_mean temp_median max_temp min_temp 
    # max_hum_max min_hum hum_mean hum_median wind_mean wind_median wind_max wind_min 
    # had_min_rain had_strong_rain days_wo_rain days_wo_strong_rain latitude_inmet longitude_inmet
    def load_to_df_inmet(self, foldername: str, file_name: str):
        column = Enum(
            'Column',
            'date time precip press max_press min_press rad temp dew_temp max_temp min_temp max_dew_temp min_dew_temp max_hum min_hum hum wind_dir wind_gust wind empty')
        df = pd.read_csv(f'{self.inmet_path}/{foldername}/{file_name}', encoding="ISO-8859-1",
                         skiprows=9, sep=';', names=[e.name for e in column], na_values=-9999)

        # Drop Unused Columns
        dropped_columns = [column.time, column.press, column.max_press, column.min_press, column.rad,
                           column.dew_temp, column.min_dew_temp, column.max_dew_temp, column.wind_dir, column.wind_gust, column.empty]
        df = df.drop(columns=[e.name for e in dropped_columns])
        
        # Convert string to float values
        for col in [column.precip, column.temp, column.max_temp, column.min_temp, column.wind]:
            df[col.name] = pd.to_numeric(df[col.name].astype(
                str).str.replace(',', '.'), errors='coerce')

        # GroupBy Day
        df = df.groupby([column.date.name], as_index=True, dropna=False).agg({
            column.precip.name: ['sum'],
            column.temp.name: ['mean', 'median'],
            column.max_temp.name: 'max',
            column.min_temp.name: 'min',
            column.max_hum.name: 'max',
            column.min_hum.name: 'min',
            column.hum.name: ['mean', 'median'],
            column.wind.name: ['mean', 'median', 'max', 'min']})

        # Fix Renamed Columns
        df.columns = df.columns.map('_'.join)
        df = df.reset_index()
        df = df.rename({
            'max_temp_max': column.max_temp.name,
            'min_temp_min': column.min_temp.name,
            'max_hum_min': column.max_hum.name,
            'min_hum_min': column.min_hum.name,
        }, axis=1)

        # Count Days Without Rain
        min_prec = 2.5
        min_strong_prec = 10

        df['had_min_rain'] = df['precip_sum'].map(
            lambda x: x >= min_prec)
        df['had_strong_rain'] = df['precip_sum'].map(
            lambda x: x >= min_strong_prec)

        df['days_wo_rain'] = ''
        df['days_wo_strong_rain'] = ''
        days_without_rain = 0
        days_without_strong_rain = 0

        for index, row in df.iterrows():
            if(row['had_min_rain']):
                days_without_rain = 0
            else:
                days_without_rain += 1

            if(row['had_strong_rain']):
                days_without_strong_rain = 0
            else:
                days_without_strong_rain += 1

            df.at[index, 'days_wo_rain'] = days_without_rain
            df.at[index, 'days_wo_strong_rain'] = days_without_strong_rain

        df = df[df['temp_mean'].notnull()]
        # Read Longitude Latitude Information
        (latitude, longitude) = self.get_coord_from_inmet_file(foldername, file_name)

        return Inmet(latitude, longitude, df.values.tolist(), df.columns)
