from data_manager.data_manager import DataManager

INMET_PATH = 'raw_data/climate-inmet'
FIRE_OUTRBREAKS_PATH = 'raw_data/fire_outbreaks-inpe'

## Available Years to Process:
# '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010'
YEARS_TO_PROCESS = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']

def run():
    print("running")

    for year_to_process in YEARS_TO_PROCESS:
        data_manager_v3 = DataManager(FIRE_OUTRBREAKS_PATH, INMET_PATH, year_to_process)  
        data_manager_v3.process_fire_outbreaks()
        data_manager_v3.process_inmet()
        data_manager_v3.process_centralized_data()

if __name__ == '__main__':
    run()