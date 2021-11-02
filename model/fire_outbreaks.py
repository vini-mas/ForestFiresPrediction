from typing import List

import pandas as pd

class FireOutbreaks():
    year: str
    state: str
    city: str
    biome: str
    latitude: float
    longitude: float

    df_list: List
    df_columns: List[str]

    def __init__(self, year: float, state: str, city: str, biome: str, latitude: float, longitude: float, df_list: List, df_columns: List[str]):
        self.year = year
        self.state = state
        self.city = city
        self.biome = biome
        self.latitude = latitude
        self.longitude = longitude

        self.df_list = df_list
        self.df_columns = df_columns

    def __str__(self):
        df = pd.DataFrame(self.df_list, columns=self.df_columns)
        return f'Year: {self.year}\nState: {self.state}\nCity: {self.city}\nBiome: {self.biome}\nLatitude: {self.latitude}\nLongitude: {self.longitude}\n DataFrame: \n{df.head()}'