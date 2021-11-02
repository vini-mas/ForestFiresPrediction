from typing import List, Tuple
import numpy as np
from pandas.core.frame import DataFrame
import progressbar
import os

from model.yearly_inmet import YearlyInmet

class Helper:
    def find_index_from_closest_coordinate(self, point: Tuple[float, float], coord_list: List[Tuple[float, float]]):
        xy = np.array(coord_list).T

        # Euclidean Distance
        d = ((xy[0] - point[0]) ** 2 + (xy[1] - point[1]) ** 2) ** 0.5

        return np.argmin(d) # Closest coordinate

    def initialize_progress_bar(self, label: str, size: int):  
        print(f'\n{label}')
        bar = progressbar.ProgressBar(maxval=size, widgets=[
            progressbar.Bar('■', ' [', ']'), ' • ', 
            progressbar.Counter(), f'/{size} - ', progressbar.Percentage(), ' • ', 
            progressbar.AdaptiveETA()],
            term_width=round(os.get_terminal_size().columns*0.8))
        bar.start()

        return bar
    
    def get_yearly_inmet_index_by_year(self, yearly_inmet_list: List[YearlyInmet], year: str):
        for index, yearly_inmet in enumerate(yearly_inmet_list):
            if(yearly_inmet.year == year):
                return index

        return -1

    def get_inmet_row_by_date(self, df: DataFrame, date: str):
        for _, row in df.iterrows():
            if(row['date'] == date):
                return row
        

