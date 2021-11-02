


from typing import List

import pandas as pd

class Inmet():
    latitude: float
    longitude: float
    df_list: List
    df_columns: List[str]

    def __init__(self, latitude: float, longitude: float, df_list: List, df_columns: List[str]):
        self.latitude = latitude
        self.longitude = longitude
        self.df_list = df_list
        self.df_columns = df_columns

    def __str__(self):
        df = pd.DataFrame(self.df_list, columns=self.df_columns)
        return f'Latitude: {self.latitude}\nLongitude: {self.longitude}\nDataFrame (head):\n{df.head()}'